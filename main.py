from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, Union, List
import json
import math
import uuid
import os
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="轻语AI飞控指挥系统",
    description="Coze平台对接后端 - 无人机智能调度系统",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 东莞地区虚拟机场配置
AIRPORTS = {
    "顶好大厦": {"lat": 22.9944, "lng": 113.7258, "name": "顶好大厦"},
    "创投大厦": {"lat": 22.9242, "lng": 113.8401, "name": "创投大厦"}, 
    "怡丰昌盛": {"lat": 23.0180, "lng": 113.7500, "name": "怡丰昌盛"}
}

# 飞行阶段定义
FLIGHT_PHASES = ["TAKEOFF", "CLIMB", "CRUISE", "LAND"]

# WebSocket连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket连接已建立，当前连接数: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket连接已断开，当前连接数: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message, ensure_ascii=False))
            except Exception as e:
                logger.error(f"WebSocket广播失败: {e}")

manager = ConnectionManager()

# 数据模型定义
class FlightDataNested(BaseModel):
    """嵌套型JSON结构"""
    lat: Union[str, float]
    lng: Union[str, float] 
    mission_id: str
    task_type: str
    timestamp: Optional[str] = None

class CommandResponse(BaseModel):
    """统一响应结构"""
    status: str
    message: str
    eta: str

def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """计算两点间距离（公里）"""
    R = 6371
    lat1_rad, lng1_rad = math.radians(lat1), math.radians(lng1)
    lat2_rad, lng2_rad = math.radians(lat2), math.radians(lng2)
    dlat, dlng = lat2_rad - lat1_rad, lng2_rad - lng1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def calculate_eta(start_lat: float, start_lng: float, target_lat: float, target_lng: float, speed_ms: float = 12) -> str:
    """计算预计到达时间"""
    distance_m = haversine_distance(start_lat, start_lng, target_lat, target_lng) * 1000
    minutes = (distance_m / speed_ms) / 60
    if minutes < 1: return "1分钟"
    if minutes < 60: return f"{int(minutes)}分钟"
    return f"{int(minutes // 60)}小时{int(minutes % 60)}分钟"

def find_nearest_airport(target_lat: float, target_lng: float) -> str:
    """找到距离目标点最近的机场"""
    min_dist, nearest = float('inf'), None
    for name, data in AIRPORTS.items():
        dist = haversine_distance(target_lat, target_lng, data["lat"], data["lng"])
        if dist < min_dist:
            min_dist, nearest = dist, name
    return nearest

def parse_coordinates(coord_data: Any) -> tuple:
    """解析坐标数据"""
    if isinstance(coord_data, str):
        try:
            parsed = json.loads(coord_data)
            return float(parsed.get('lat', 0)), float(parsed.get('lng', 0))
        except:
            if ',' in coord_data:
                lat, lng = coord_data.split(',')
                return float(lat.strip()), float(lng.strip())
    elif isinstance(coord_data, dict):
        return float(coord_data.get('lat', 0)), float(coord_data.get('lng', 0))
    return 0.0, 0.0

@app.post("/drone/command", response_model=CommandResponse)
async def drone_command(request_data: Dict[str, Any]):
    """无人机指令接口"""
    try:
        logger.info(f"收到指令数据: {request_data}")
        
        target_lat, target_lng = 0.0, 0.0
        mission_id = str(uuid.uuid4())
        task_type = "patrol"
        
        # 核心逻辑：匹配扣子传过来的 flight_data (注意下划线)
        if "flight_data" in request_data:
            fd = request_data["flight_data"]
            target_lat = float(fd.get("lat", 0))
            target_lng = float(fd.get("lng", 0))
            mission_id = fd.get("mission_id", mission_id)
            task_type = fd.get("task_type", task_type)
            logger.info(f"解析成功 - 任务ID: {mission_id}, 坐标: ({target_lat}, {target_lng})")
        else:
            # 兼容扁平结构
            target_lat = float(request_data.get("lat", 0))
            target_lng = float(request_data.get("lng", 0))
            mission_id = request_data.get("mission_id", mission_id)
            task_type = request_data.get("task_type", task_type)

        if target_lat == 0.0 and target_lng == 0.0:
            raise HTTPException(status_code=400, detail="无效的目标坐标")
        
        # 智能调度
        selected_airport = find_nearest_airport(target_lat, target_lng)
        airport_info = AIRPORTS[selected_airport]
        
        # 计算时间
        eta = calculate_eta(airport_info["lat"], airport_info["lng"], target_lat, target_lng)
        
        # WebSocket广播实时状态
        websocket_payload = {
            "event": "flight_start",
            "payload": {
                "mission_id": mission_id,
                "selected_airport": selected_airport,
                "target_coordinates": {"lat": target_lat, "lng": target_lng},
                "task_type": task_type,
                "timestamp": datetime.now().isoformat()
            }
        }
        await manager.broadcast(websocket_payload)
        
        return CommandResponse(status="success", message="指令执行成功", eta=eta)
        
    except Exception as e:
        logger.error(f"处理指令发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    return {"system": "轻语AI飞控指挥系统", "status": "online", "connections": len(manager.active_connections)}

if __name__ == "__main__":
    import uvicorn
    # 适配 Zeabur 端口
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)