from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Union, List
import json
import math
import asyncio
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
    """嵌套型JSON结构A"""
    lat: Union[str, float]
    lng: Union[str, float] 
    mission_id: str
    task_type: str

class CommandRequestNested(BaseModel):
    """嵌套型请求结构"""
    flight_data: FlightDataNested

class CommandRequestFlat(BaseModel):
    """扁平型请求结构B"""
    target_coordinate: Union[str, Dict[str, Union[str, float]]]
    mission_id: Optional[str] = None
    task_type: Optional[str] = "patrol"
    
class ExecutedCommand(BaseModel):
    """执行的指令信息"""
    mission_id: str
    lat: str
    lng: str

class CommandResponse(BaseModel):
    """统一响应结构"""
    status: str
    message: str
    eta: str

def calculate_eta(start_lat: float, start_lng: float, target_lat: float, target_lng: float, speed_ms: float = 12) -> str:
    """
    计算预计到达时间（ETA）
    
    Args:
        start_lat: 起始纬度
        start_lng: 起始经度
        target_lat: 目标纬度
        target_lng: 目标经度
        speed_ms: 无人机速度（米/秒），默认12m/s
    
    Returns:
        str: 格式化的ETA时间，如"12分钟"
    """
    # 计算距离（米）
    distance_km = haversine_distance(start_lat, start_lng, target_lat, target_lng)
    distance_m = distance_km * 1000
    
    # 计算飞行时间（秒）
    flight_time_seconds = distance_m / speed_ms
    
    # 转换为分钟
    flight_time_minutes = flight_time_seconds / 60
    
    # 格式化输出
    if flight_time_minutes < 1:
        return "1分钟"
    elif flight_time_minutes < 60:
        return f"{int(flight_time_minutes)}分钟"
    else:
        hours = int(flight_time_minutes // 60)
        minutes = int(flight_time_minutes % 60)
        if minutes == 0:
            return f"{hours}小时"
        else:
            return f"{hours}小时{minutes}分钟"

def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    使用Haversine公式计算两点间距离（公里）
    """
    R = 6371  # 地球半径（公里）
    
    # 转换为弧度
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    # Haversine公式
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def find_nearest_airport(target_lat: float, target_lng: float) -> str:
    """
    找到距离目标点最近的机场
    """
    min_distance = float('inf')
    nearest_airport = None
    
    for airport_name, airport_data in AIRPORTS.items():
        distance = haversine_distance(
            target_lat, target_lng,
            airport_data["lat"], airport_data["lng"]
        )
        
        if distance < min_distance:
            min_distance = distance
            nearest_airport = airport_name
    
    logger.info(f"最近机场: {nearest_airport}, 距离: {min_distance:.2f}km")
    return nearest_airport

def security_audit(target_lat: float, target_lng: float, task_type: str) -> bool:
    """
    安全审计函数 - 目前默认通过，预留气象和禁飞区校验逻辑
    """
    # TODO: 实现气象条件检查
    # TODO: 实现禁飞区检查
    # TODO: 实现飞行高度限制检查
    
    logger.info(f"安全审计通过 - 目标坐标: ({target_lat}, {target_lng}), 任务类型: {task_type}")
    return True

def generate_flight_sequence() -> List[str]:
    """
    生成模拟飞行序列
    """
    return FLIGHT_PHASES.copy()

def parse_coordinates(coord_data: Union[str, Dict, float]) -> tuple:
    """
    解析坐标数据，支持多种格式
    """
    if isinstance(coord_data, str):
        try:
            # 尝试解析JSON字符串
            parsed = json.loads(coord_data)
            if isinstance(parsed, dict):
                return float(parsed.get('lat', 0)), float(parsed.get('lng', 0))
            # 尝试解析逗号分隔的字符串 "lat,lng"
            elif ',' in coord_data:
                lat, lng = coord_data.split(',')
                return float(lat.strip()), float(lng.strip())
        except:
            pass
    elif isinstance(coord_data, dict):
        return float(coord_data.get('lat', 0)), float(coord_data.get('lng', 0))
    
    return 0.0, 0.0
@app.post("/drone/command", response_model=CommandResponse)
async def drone_command(request_data: Dict[str, Any]):
    """
    无人机指令接口 - 支持两种JSON结构的鲁棒性解析
    """
    try:
        logger.info(f"收到指令: {request_data}")
        
        # 解析目标坐标和任务信息
        target_lat, target_lng = 0.0, 0.0
        mission_id = str(uuid.uuid4())
        task_type = "patrol"
        
        # 结构A检测（嵌套型）
        if "flight_data" in request_data:
            flight_data = request_data["flight_data"]
            target_lat = float(flight_data.get("lat", 0))
            target_lng = float(flight_data.get("lng", 0))
            mission_id = flight_data.get("mission_id", mission_id)
            task_type = flight_data.get("task_type", task_type)
            logger.info("检测到结构A（嵌套型）")
            
        # 结构B检测（扁平型）
        elif "target_coordinate" in request_data:
            target_lat, target_lng = parse_coordinates(request_data["target_coordinate"])
            mission_id = request_data.get("mission_id", mission_id)
            task_type = request_data.get("task_type", task_type)
            logger.info("检测到结构B（扁平型）")
            
        # 其他可能的扁平结构
        elif "lat" in request_data and "lng" in request_data:
            target_lat = float(request_data.get("lat", 0))
            target_lng = float(request_data.get("lng", 0))
            mission_id = request_data.get("mission_id", mission_id)
            task_type = request_data.get("task_type", task_type)
            logger.info("检测到直接坐标结构")
            
        else:
            raise HTTPException(status_code=400, detail="无法解析坐标信息")
        
        # 坐标有效性检查
        if target_lat == 0.0 and target_lng == 0.0:
            raise HTTPException(status_code=400, detail="无效的目标坐标")
        
        # 安全审计
        if not security_audit(target_lat, target_lng, task_type):
            raise HTTPException(status_code=403, detail="安全审计未通过")
        
        # 智能调度 - 选择最近机场
        selected_airport = find_nearest_airport(target_lat, target_lng)
        
        # 获取选定机场的坐标
        airport_info = AIRPORTS[selected_airport]
        airport_lat = airport_info["lat"]
        airport_lng = airport_info["lng"]
        
        # 计算ETA（从机场到目标点的飞行时间）
        eta = calculate_eta(airport_lat, airport_lng, target_lat, target_lng)
        
        # 生成飞行序列
        flight_sequence = generate_flight_sequence()
        
        # 构建响应 - 按照新的格式要求
        response = CommandResponse(
            status="success",
            message="指令执行成功",
            eta=eta
        )
        
        # WebSocket广播
        websocket_payload = {
            "event": "flight_start",
            "payload": {
                "mission_id": mission_id,
                "selected_airport": selected_airport,
                "airport_coordinates": AIRPORTS[selected_airport],
                "target_coordinates": {"lat": target_lat, "lng": target_lng},
                "task_type": task_type,
                "flight_sequence": flight_sequence,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        await manager.broadcast(websocket_payload)
        logger.info(f"任务 {mission_id} 已广播到WebSocket客户端")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理指令时发生错误: {e}")
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket连接端点
    """
    await manager.connect(websocket)
    try:
        while True:
            # 保持连接活跃
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def root():
    """
    根路径 - 系统状态
    """
    return {
        "system": "轻语AI飞控指挥系统",
        "status": "运行中",
        "version": "1.0.0",
        "airports": list(AIRPORTS.keys()),
        "websocket_connections": len(manager.active_connections)
    }

@app.get("/airports")
async def get_airports():
    """
    获取所有机场信息
    """
    return {"airports": AIRPORTS}

@app.get("/health")
async def health_check():
    """
    健康检查
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)