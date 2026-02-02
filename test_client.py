#!/usr/bin/env python3
"""
福华创新AI飞控指挥系统 - 测试客户端
"""

import requests
import json
import asyncio
import websockets
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws"

def test_api_structure_a():
    """测试结构A（嵌套型）"""
    print("=== 测试结构A（嵌套型） ===")
    
    payload = {
        "flight_data": {
            "lat": "22.9500",
            "lng": "113.7600", 
            "mission_id": "test_mission_a",
            "task_type": "patrol"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/drone/command", json=payload)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {e}")

def test_api_structure_b():
    """测试结构B（扁平型）"""
    print("\n=== 测试结构B（扁平型） ===")
    
    payload = {
        "target_coordinate": "22.9200,113.8300",
        "mission_id": "test_mission_b", 
        "task_type": "surveillance"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/drone/command", json=payload)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {e}")

def test_api_structure_b_json_coord():
    """测试结构B（JSON坐标格式）"""
    print("\n=== 测试结构B（JSON坐标格式） ===")
    
    payload = {
        "target_coordinate": {"lat": 23.0100, "lng": 113.7400},
        "mission_id": "test_mission_c",
        "task_type": "emergency"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/drone/command", json=payload)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {e}")

def test_system_status():
    """测试系统状态"""
    print("\n=== 测试系统状态 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"系统状态: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        response = requests.get(f"{BASE_URL}/airports")
        print(f"机场信息: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        response = requests.get(f"{BASE_URL}/health")
        print(f"健康检查: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {e}")

async def test_websocket():
    """测试WebSocket连接"""
    print("\n=== 测试WebSocket连接 ===")
    
    try:
        async with websockets.connect(WS_URL) as websocket:
            print("WebSocket连接成功")
            
            # 发送一个API请求来触发WebSocket消息
            payload = {
                "flight_data": {
                    "lat": "22.9800",
                    "lng": "113.7200",
                    "mission_id": "websocket_test",
                    "task_type": "test"
                }
            }
            
            # 在另一个线程中发送API请求
            import threading
            def send_api_request():
                requests.post(f"{BASE_URL}/drone/command", json=payload)
            
            thread = threading.Thread(target=send_api_request)
            thread.start()
            
            # 等待WebSocket消息
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"收到WebSocket消息: {json.dumps(json.loads(message), indent=2, ensure_ascii=False)}")
            except asyncio.TimeoutError:
                print("WebSocket消息接收超时")
            
            thread.join()
            
    except Exception as e:
        print(f"WebSocket测试失败: {e}")

def main():
    """主测试函数"""
    print("福华创新AI飞控指挥系统 - 功能测试")
    print("=" * 50)
    
    # 测试系统状态
    test_system_status()
    
    # 测试API接口
    test_api_structure_a()
    test_api_structure_b() 
    test_api_structure_b_json_coord()
    
    # 测试WebSocket
    print("\n启动WebSocket测试...")
    asyncio.run(test_websocket())
    
    print("\n测试完成！")

if __name__ == "__main__":
    main()