#!/usr/bin/env python3
"""
测试新的响应格式
"""

import json
import urllib.request

def test_new_format():
    """测试新的响应格式"""
    
    # 测试数据
    test_data = {
        "flight_data": {
            "lat": "22.87",
            "lng": "113.86", 
            "mission_id": "AUTO_GEN_123",
            "task_type": "patrol"
        }
    }
    
    try:
        # 发送请求
        data = json.dumps(test_data).encode('utf-8')
        req = urllib.request.Request('http://localhost:8000/drone/command', data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            print("📋 测试新响应格式")
            print("=" * 50)
            print("发送数据:", json.dumps(test_data, indent=2, ensure_ascii=False))
            print("\n收到响应:", json.dumps(result, indent=2, ensure_ascii=False))
            
            # 验证格式
            if "executed_command" in result:
                print("\n✅ 新格式验证成功！")
                print(f"   状态: {result['status']}")
                print(f"   任务ID: {result['executed_command']['mission_id']}")
                print(f"   坐标: ({result['executed_command']['lat']}, {result['executed_command']['lng']})")
            else:
                print("\n❌ 还是旧格式")
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_new_format()