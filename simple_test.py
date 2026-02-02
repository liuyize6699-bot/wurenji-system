#!/usr/bin/env python3
"""
简单测试脚本 - 仅使用Python标准库
"""

import json
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError

BASE_URL = "http://localhost:8000"

def test_request(url, data=None, method="GET"):
    """发送HTTP请求"""
    try:
        if data:
            data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(url, data=data, method=method)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib.request.Request(url, method=method)
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return response.status, result
            
    except HTTPError as e:
        error_data = json.loads(e.read().decode('utf-8'))
        return e.code, error_data
    except URLError as e:
        return None, {"error": f"连接失败: {e.reason}"}
    except Exception as e:
        return None, {"error": f"请求失败: {str(e)}"}

def test_system_status():
    """测试系统状态"""
    print("=== 测试系统状态 ===")
    
    # 测试根路径
    status, result = test_request(f"{BASE_URL}/")
    print(f"系统状态 [{status}]: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 测试机场信息
    status, result = test_request(f"{BASE_URL}/airports")
    print(f"机场信息 [{status}]: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 测试健康检查
    status, result = test_request(f"{BASE_URL}/health")
    print(f"健康检查 [{status}]: {json.dumps(result, indent=2, ensure_ascii=False)}")

def test_structure_a():
    """测试结构A（嵌套型）"""
    print("\n=== 测试结构A（嵌套型） ===")
    
    payload = {
        "flight_data": {
            "lat": "22.9500",
            "lng": "113.7600",
            "mission_id": "test_mission_a",
            "task_type": "patrol"
        }
    }
    
    status, result = test_request(f"{BASE_URL}/drone/command", payload, "POST")
    print(f"响应 [{status}]: {json.dumps(result, indent=2, ensure_ascii=False)}")

def test_structure_b():
    """测试结构B（扁平型）"""
    print("\n=== 测试结构B（扁平型） ===")
    
    payload = {
        "target_coordinate": "22.9200,113.8300",
        "mission_id": "test_mission_b",
        "task_type": "surveillance"
    }
    
    status, result = test_request(f"{BASE_URL}/drone/command", payload, "POST")
    print(f"响应 [{status}]: {json.dumps(result, indent=2, ensure_ascii=False)}")

def test_structure_b_json():
    """测试结构B（JSON坐标）"""
    print("\n=== 测试结构B（JSON坐标） ===")
    
    payload = {
        "target_coordinate": {"lat": 23.0100, "lng": 113.7400},
        "mission_id": "test_mission_c",
        "task_type": "emergency"
    }
    
    status, result = test_request(f"{BASE_URL}/drone/command", payload, "POST")
    print(f"响应 [{status}]: {json.dumps(result, indent=2, ensure_ascii=False)}")

def test_direct_coordinates():
    """测试直接坐标格式"""
    print("\n=== 测试直接坐标格式 ===")
    
    payload = {
        "lat": 22.9800,
        "lng": 113.7200,
        "mission_id": "test_mission_d",
        "task_type": "inspection"
    }
    
    status, result = test_request(f"{BASE_URL}/drone/command", payload, "POST")
    print(f"响应 [{status}]: {json.dumps(result, indent=2, ensure_ascii=False)}")

def test_error_case():
    """测试错误情况"""
    print("\n=== 测试错误情况 ===")
    
    payload = {
        "invalid_data": "test"
    }
    
    status, result = test_request(f"{BASE_URL}/drone/command", payload, "POST")
    print(f"错误响应 [{status}]: {json.dumps(result, indent=2, ensure_ascii=False)}")

def main():
    """主测试函数"""
    print("福华创新AI飞控指挥系统 - 简单测试")
    print("=" * 50)
    print("请确保服务器已启动: python simple_server.py")
    print("=" * 50)
    
    # 测试系统状态
    test_system_status()
    
    # 测试各种API格式
    test_structure_a()
    test_structure_b()
    test_structure_b_json()
    test_direct_coordinates()
    
    # 测试错误情况
    test_error_case()
    
    print("\n测试完成！")
    print("\n距离计算验证:")
    print("- 目标点 (22.9500, 113.7600) 最近机场应该是: 顶好大厦")
    print("- 目标点 (22.9200, 113.8300) 最近机场应该是: 创投大厦")
    print("- 目标点 (23.0100, 113.7400) 最近机场应该是: 怡丰昌盛")

if __name__ == "__main__":
    main()