#!/usr/bin/env python3
import json
import urllib.request

# 简单测试ETA功能
data = {
    "flight_data": {
        "lat": "22.95",
        "lng": "113.76",
        "mission_id": "ETA_TEST",
        "task_type": "patrol"
    }
}

try:
    req = urllib.request.Request('http://localhost:8000/drone/command', 
                                data=json.dumps(data).encode(), method='POST')
    req.add_header('Content-Type', 'application/json')
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print("ETA测试结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
except Exception as e:
    print(f"测试失败: {e}")