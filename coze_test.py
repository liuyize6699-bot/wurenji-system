#!/usr/bin/env python3
"""
模拟扣子平台调用测试
"""

import json
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError
import time

BASE_URL = "http://localhost:8000"

def simulate_coze_call(lat, lng, task_type="patrol"):
    """模拟扣子平台的API调用"""
    
    # 生成任务ID（模拟扣子的方式）
    mission_id = f"coze_{int(time.time())}"
    
    # 构建请求数据（使用嵌套结构A）
    request_data = {
        "flight_data": {
            "lat": str(lat),
            "lng": str(lng), 
            "mission_id": mission_id,
            "task_type": task_type
        }
    }
    
    print(f"🤖 扣子平台发送请求:")
    print(f"📍 目标坐标: ({lat}, {lng})")
    print(f"🎯 任务类型: {task_type}")
    print(f"🆔 任务ID: {mission_id}")
    print("-" * 50)
    
    try:
        # 发送HTTP请求
        data = json.dumps(request_data).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/drone/command", data=data, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # 模拟扣子处理响应
            if result.get('status') == 'success':
                print("✅ 飞行任务调度成功！")
                print(f"🛫 起飞机场: {result['selected_airport']}")
                print(f"🎯 目标坐标: ({result['target_coordinates']['lat']}, {result['target_coordinates']['lng']})")
                print(f"🛩️ 飞行序列: {' → '.join(result['flight_sequence'])}")
                print(f"⏰ 创建时间: {result['timestamp']}")
                
                # 模拟扣子的回复消息
                reply_message = f"""✅ 飞行任务调度成功！

📍 任务ID: {result['mission_id']}
🛫 起飞机场: {result['selected_airport']}
🎯 目标坐标: ({result['target_coordinates']['lat']}, {result['target_coordinates']['lng']})
🛩️ 飞行序列: {' → '.join(result['flight_sequence'])}
⏰ 创建时间: {result['timestamp']}"""
                
                print("\n🤖 扣子回复用户:")
                print(reply_message)
                
            else:
                print(f"❌ 任务调度失败: {result.get('message', '未知错误')}")
                
            return result
            
    except Exception as e:
        error_msg = f"❌ 连接飞控系统失败: {str(e)}"
        print(error_msg)
        return {"status": "error", "message": error_msg}

def test_multiple_scenarios():
    """测试多种场景"""
    
    print("=" * 60)
    print("🚁 福华创新AI飞控指挥系统 - 扣子平台对接测试")
    print("=" * 60)
    
    # 测试场景1：巡逻任务
    print("\n📋 场景1: 巡逻任务")
    simulate_coze_call(22.9500, 113.7600, "patrol")
    
    print("\n" + "="*60)
    
    # 测试场景2：监控任务
    print("\n📋 场景2: 监控任务")
    simulate_coze_call(22.9200, 113.8300, "surveillance")
    
    print("\n" + "="*60)
    
    # 测试场景3：紧急任务
    print("\n📋 场景3: 紧急任务")
    simulate_coze_call(23.0100, 113.7400, "emergency")
    
    print("\n" + "="*60)
    
    # 测试场景4：检查任务
    print("\n📋 场景4: 检查任务")
    simulate_coze_call(22.9800, 113.7200, "inspection")

def test_user_interaction():
    """模拟用户交互"""
    print("\n" + "="*60)
    print("🗣️ 模拟用户对话")
    print("="*60)
    
    # 模拟用户输入
    user_inputs = [
        {
            "message": "我需要在东莞市中心执行巡逻任务",
            "extracted": {"lat": 22.9500, "lng": 113.7600, "task_type": "patrol"}
        },
        {
            "message": "紧急！需要在创投大厦附近进行监控",
            "extracted": {"lat": 22.9242, "lng": 113.8401, "task_type": "emergency"}
        }
    ]
    
    for i, interaction in enumerate(user_inputs, 1):
        print(f"\n👤 用户输入 {i}: {interaction['message']}")
        print("🤖 扣子解析结果:")
        print(f"   纬度: {interaction['extracted']['lat']}")
        print(f"   经度: {interaction['extracted']['lng']}")
        print(f"   任务类型: {interaction['extracted']['task_type']}")
        
        print("\n🤖 扣子调用飞控API:")
        simulate_coze_call(
            interaction['extracted']['lat'],
            interaction['extracted']['lng'], 
            interaction['extracted']['task_type']
        )
        
        if i < len(user_inputs):
            print("\n" + "-"*40)

if __name__ == "__main__":
    # 检查服务是否运行
    try:
        req = urllib.request.Request(f"{BASE_URL}/health")
        with urllib.request.urlopen(req) as response:
            health = json.loads(response.read().decode('utf-8'))
            if health.get('status') == 'healthy':
                print("✅ 飞控系统运行正常")
            else:
                print("⚠️ 飞控系统状态异常")
                exit(1)
    except:
        print("❌ 无法连接飞控系统，请先启动服务: py simple_server.py")
        exit(1)
    
    # 运行测试
    test_multiple_scenarios()
    test_user_interaction()
    
    print("\n" + "="*60)
    print("🎉 扣子平台对接测试完成！")
    print("📖 查看 COZE_INTEGRATION.md 了解详细对接步骤")
    print("="*60)