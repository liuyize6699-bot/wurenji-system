#!/usr/bin/env python3
"""
测试速度变化对ETA的影响
"""

import json
import urllib.request

def test_eta_with_new_speed():
    """测试新速度下的ETA计算"""
    
    test_cases = [
        {
            "name": "近距离测试",
            "data": {
                "flight_data": {
                    "lat": "22.95",
                    "lng": "113.76",
                    "mission_id": "SPEED_TEST_1",
                    "task_type": "patrol"
                }
            }
        },
        {
            "name": "中距离测试",
            "data": {
                "flight_data": {
                    "lat": "22.92",
                    "lng": "113.84",
                    "mission_id": "SPEED_TEST_2",
                    "task_type": "surveillance"
                }
            }
        },
        {
            "name": "远距离测试（广州）",
            "data": {
                "flight_data": {
                    "lat": "23.1291",
                    "lng": "113.2644",
                    "mission_id": "SPEED_TEST_3",
                    "task_type": "inspection"
                }
            }
        }
    ]
    
    print("🚁 轻语AI飞控指挥系统 - 速度调整验证")
    print("=" * 60)
    print("新速度设定: 12m/s (43.2km/h)")
    print("原速度设定: 20m/s (72km/h)")
    print("理论ETA增加: 约67%")
    print("=" * 60)
    
    for test_case in test_cases:
        try:
            req = urllib.request.Request('http://localhost:8000/drone/command',
                                        data=json.dumps(test_case["data"]).encode(),
                                        method='POST')
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                
                print(f"\n📋 {test_case['name']}")
                print("-" * 40)
                lat = test_case["data"]["flight_data"]["lat"]
                lng = test_case["data"]["flight_data"]["lng"]
                print(f"目标坐标: ({lat}, {lng})")
                print(f"ETA (12m/s): {result.get('eta', '未知')}")
                
        except Exception as e:
            print(f"❌ {test_case['name']} 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 速度对比说明:")
    print("- 12m/s = 43.2km/h (新设定)")
    print("- 20m/s = 72.0km/h (原设定)")
    print("- 速度降低40%，ETA相应增加约67%")
    print("- 更符合实际无人机巡航速度")
    print("=" * 60)

if __name__ == "__main__":
    test_eta_with_new_speed()