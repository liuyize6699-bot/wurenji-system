#!/usr/bin/env python3
"""
测试ETA（预计到达时间）功能
"""

import json
import urllib.request

def test_eta(name, data, expected_airport):
    """测试ETA计算"""
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request('http://localhost:8000/drone/command', data=json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            print(f"\n📋 {name}")
            print("=" * 50)
            print("发送数据:", json.dumps(data, indent=2, ensure_ascii=False))
            print("\n收到响应:", json.dumps(result, indent=2, ensure_ascii=False))
            
            if "eta" in result:
                print(f"✅ ETA计算成功: {result['eta']}")
                print(f"📍 预期选择机场: {expected_airport}")
            else:
                print("❌ 缺少ETA字段")
                
    except Exception as e:
        print(f"❌ {name} 测试失败: {e}")

def main():
    print("🚁 轻语AI飞控指挥系统 - ETA功能测试")
    print("=" * 60)
    print("无人机速度设定: 20m/s (72km/h)")
    print("=" * 60)
    
    # 测试1: 近距离目标（顶好大厦附近）
    test_eta("近距离目标 - 顶好大厦附近", {
        "flight_data": {
            "lat": "22.9950",  # 接近顶好大厦
            "lng": "113.7260",
            "mission_id": "ETA_TEST_001",
            "task_type": "patrol"
        }
    }, "顶好大厦")
    
    # 测试2: 中距离目标（创投大厦附近）
    test_eta("中距离目标 - 创投大厦附近", {
        "flight_data": {
            "lat": "22.9200",  # 接近创投大厦
            "lng": "113.8400",
            "mission_id": "ETA_TEST_002",
            "task_type": "surveillance"
        }
    }, "创投大厦")
    
    # 测试3: 远距离目标（怡丰昌盛附近）
    test_eta("远距离目标 - 怡丰昌盛附近", {
        "flight_data": {
            "lat": "23.0200",  # 接近怡丰昌盛
            "lng": "113.7500",
            "mission_id": "ETA_TEST_003",
            "task_type": "emergency"
        }
    }, "怡丰昌盛")
    
    # 测试4: 超远距离目标（测试小时显示）
    test_eta("超远距离目标 - 广州市中心", {
        "flight_data": {
            "lat": "23.1291",  # 广州市中心
            "lng": "113.2644",
            "mission_id": "ETA_TEST_004",
            "task_type": "inspection"
        }
    }, "怡丰昌盛")
    
    print("\n" + "=" * 60)
    print("🎯 ETA计算说明:")
    print("- 基于Haversine公式计算直线距离")
    print("- 无人机速度: 20m/s (约72km/h)")
    print("- 从选定机场到目标点的飞行时间")
    print("- 自动格式化为分钟或小时分钟")
    print("=" * 60)

if __name__ == "__main__":
    main()