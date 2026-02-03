#!/usr/bin/env python3
"""
轻语AI飞控指挥系统 - 简化版（仅使用Python标准库）
适用于快速测试，无需安装额外依赖
"""

import json
import math
import uuid
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import socket

# 东莞地区虚拟机场配置
AIRPORTS = {
    "顶好大厦": {"lat": 22.9944, "lng": 113.7258, "name": "顶好大厦"},
    "创投大厦": {"lat": 22.9242, "lng": 113.8401, "name": "创投大厦"}, 
    "怡丰昌盛": {"lat": 23.0180, "lng": 113.7500, "name": "怡丰昌盛"}
}

FLIGHT_PHASES = ["TAKEOFF", "CLIMB", "CRUISE", "LAND"]

def haversine_distance(lat1, lng1, lat2, lng2):
    """计算两点间距离（公里）"""
    R = 6371  # 地球半径
    
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def calculate_eta(start_lat, start_lng, target_lat, target_lng, speed_ms=12):
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

def find_nearest_airport(target_lat, target_lng):
    """找到最近的机场"""
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
    
    print(f"最近机场: {nearest_airport}, 距离: {min_distance:.2f}km")
    return nearest_airport

def parse_coordinates(coord_data):
    """解析坐标数据"""
    if isinstance(coord_data, str):
        try:
            # 先尝试解析逗号分隔的字符串
            if ',' in coord_data:
                lat, lng = coord_data.split(',')
                return float(lat.strip()), float(lng.strip())
            # 再尝试解析JSON字符串
            parsed = json.loads(coord_data)
            if isinstance(parsed, dict):
                return float(parsed.get('lat', 0)), float(parsed.get('lng', 0))
        except:
            pass
    elif isinstance(coord_data, dict):
        return float(coord_data.get('lat', 0)), float(coord_data.get('lng', 0))
    
    return 0.0, 0.0

class DroneCommandHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            response = {
                "system": "轻语AI飞控指挥系统",
                "status": "运行中",
                "version": "1.0.0-simple",
                "airports": list(AIRPORTS.keys())
            }
        elif parsed_path.path == '/airports':
            response = {"airports": AIRPORTS}
        elif parsed_path.path == '/health':
            response = {"status": "healthy", "timestamp": datetime.now().isoformat()}
        else:
            self.send_error(404, "Not Found")
            return
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def do_POST(self):
        """处理POST请求"""
        if self.path != '/drone/command':
            self.send_error(404, "Not Found")
            return
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            print("【收到无人机指令】:", request_data)
            
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
                print("检测到结构A（嵌套型）")
                
            # 结构B检测（扁平型）
            elif "target_coordinate" in request_data:
                target_lat, target_lng = parse_coordinates(request_data["target_coordinate"])
                mission_id = request_data.get("mission_id", mission_id)
                task_type = request_data.get("task_type", task_type)
                print("检测到结构B（扁平型）")
                
            # 其他可能的扁平结构
            elif "lat" in request_data and "lng" in request_data:
                target_lat = float(request_data.get("lat", 0))
                target_lng = float(request_data.get("lng", 0))
                mission_id = request_data.get("mission_id", mission_id)
                task_type = request_data.get("task_type", task_type)
                print("检测到直接坐标结构")
                
            else:
                raise ValueError("无法解析坐标信息")
            
            # 坐标有效性检查
            if target_lat == 0.0 and target_lng == 0.0:
                raise ValueError("无效的目标坐标")
            
            # 智能调度 - 选择最近机场
            selected_airport = find_nearest_airport(target_lat, target_lng)
            
            # 获取选定机场的坐标
            airport_info = AIRPORTS[selected_airport]
            airport_lat = airport_info["lat"]
            airport_lng = airport_info["lng"]
            
            # 计算ETA（从机场到目标点的飞行时间）
            eta = calculate_eta(airport_lat, airport_lng, target_lat, target_lng)
            
            # 构建响应 - 按照新的格式要求
            response = {
                "status": "success",
                "message": "指令执行成功",
                "eta": eta
            }
            
            print(f"任务 {mission_id} 处理完成，选定机场: {selected_airport}")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            print(f"处理指令时发生错误: {e}")
            error_response = {
                "status": "error",
                "message": f"处理失败: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            
            self.send_response(400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

import os

def run_server(port=None):
    """启动服务器"""
    if port is None:
        port = int(os.environ.get("PORT", 8000))
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, DroneCommandHandler)
    
    print("=" * 60)
    print("🚁 轻语AI飞控指挥系统 (简化版)")
    print("=" * 60)
    print(f"🌐 服务地址: http://0.0.0.0:{port}")
    print(f"📋 系统状态: http://0.0.0.0:{port}/")
    print(f"✈️  机场信息: http://0.0.0.0:{port}/airports")
    print(f"❤️  健康检查: http://0.0.0.0:{port}/health")
    print("=" * 60)
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()