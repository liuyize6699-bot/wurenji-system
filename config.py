"""
福华创新AI飞控指挥系统 - 配置文件
"""

import os
from typing import Dict, Any

class Config:
    """系统配置类"""
    
    # 服务器配置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # 东莞地区虚拟机场配置
    AIRPORTS = {
        "顶好大厦": {
            "lat": float(os.getenv("AIRPORT_1_LAT", 22.9944)),
            "lng": float(os.getenv("AIRPORT_1_LNG", 113.7258)),
            "name": "顶好大厦",
            "code": "DH"
        },
        "创投大厦": {
            "lat": float(os.getenv("AIRPORT_2_LAT", 22.9242)),
            "lng": float(os.getenv("AIRPORT_2_LNG", 113.8401)),
            "name": "创投大厦", 
            "code": "CT"
        },
        "怡丰昌盛": {
            "lat": float(os.getenv("AIRPORT_3_LAT", 23.0180)),
            "lng": float(os.getenv("AIRPORT_3_LNG", 113.7500)),
            "name": "怡丰昌盛",
            "code": "YF"
        }
    }
    
    # 飞行参数配置
    FLIGHT_PHASES = ["TAKEOFF", "CLIMB", "CRUISE", "LAND"]
    MAX_FLIGHT_DISTANCE = float(os.getenv("MAX_FLIGHT_DISTANCE", 100))  # 最大飞行距离(km)
    MIN_FLIGHT_ALTITUDE = int(os.getenv("MIN_FLIGHT_ALTITUDE", 50))     # 最小飞行高度(m)
    MAX_FLIGHT_ALTITUDE = int(os.getenv("MAX_FLIGHT_ALTITUDE", 500))    # 最大飞行高度(m)
    
    # 安全配置
    ENABLE_SECURITY_AUDIT = os.getenv("ENABLE_SECURITY_AUDIT", "True").lower() == "true"
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    NO_FLY_ZONES = []  # 禁飞区配置，可从环境变量或数据库加载
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "flight_control.log")
    
    # WebSocket配置
    WS_MAX_CONNECTIONS = int(os.getenv("WS_MAX_CONNECTIONS", 100))
    WS_HEARTBEAT_INTERVAL = int(os.getenv("WS_HEARTBEAT_INTERVAL", 30))
    
    @classmethod
    def get_airport_by_name(cls, name: str) -> Dict[str, Any]:
        """根据名称获取机场信息"""
        return cls.AIRPORTS.get(name, {})
    
    @classmethod
    def get_all_airports(cls) -> Dict[str, Dict[str, Any]]:
        """获取所有机场信息"""
        return cls.AIRPORTS
    
    @classmethod
    def validate_coordinates(cls, lat: float, lng: float) -> bool:
        """验证坐标是否在合理范围内（东莞地区）"""
        # 东莞地区大致范围
        return (22.5 <= lat <= 23.5) and (113.5 <= lng <= 114.5)

# 创建全局配置实例
config = Config()