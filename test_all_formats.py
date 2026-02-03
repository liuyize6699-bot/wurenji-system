#!/usr/bin/env python3
"""
测试所有格式的新响应
"""

import json
import urllib.request

def test_format(name, data):
    """测试指定格式"""
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request('http://localhost:8000/drone/command', data=json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            print(f"\n📋 {name}")
            print("=" * 40)
            print("响应:", json.dumps(result, indent=2, ensure_ascii=False))
            
            if "executed_command" in result:
                print("✅ 新格式正确")
            else:
                print("❌ 格式错误")
                
    except Exception as e:
        print(f"❌ {name} 测试失败: {e}")

def main():
    print("🚁 轻语AI飞控指挥系统 - 新响应格式测试")
    print("=" * 60)
    
    # 测试格式A（嵌套型）
    test_format("格式A（嵌套型）", {
        "flight_data": {
            "lat": "22.87",
            "lng": "113.86",
            "mission_id": "AUTO_GEN_123",
            "task_type": "patrol"
        }
    })
    
    # 测试格式B（扁平字符串）
    test_format("格式B（扁平字符串）", {
        "target_coordinate": "22.92,113.83",
        "mission_id": "AUTO_GEN_456",
        "task_type": "surveillance"
    })
    
    # 测试格式B（JSON对象）
    test_format("格式B（JSON对象）", {
        "target_coordinate": {"lat": 23.01, "lng": 113.74},
        "mission_id": "AUTO_GEN_789",
        "task_type": "emergency"
    })
    
    # 测试直接坐标
    test_format("直接坐标格式", {
        "lat": 22.98,
        "lng": 113.72,
        "mission_id": "AUTO_GEN_999",
        "task_type": "inspection"
    })

if __name__ == "__main__":
    main()