#!/usr/bin/env python3
"""
AirSim 简单起飞测试 - 最小化版本
不使用 numpy，只使用 Python 内置库
"""

import time
import math

try:
    import airsim
    print("✅ AirSim 已导入")
except ImportError:
    print("❌ 请先安装 AirSim: pip install airsim")
    exit(1)

def simple_takeoff():
    """简单的起飞测试"""
    
    print("\n🚁 连接到 AirSim...")
    client = airsim.MultirotorClient()
    client.confirmConnection()
    print("✅ 连接成功")
    
    print("\n🔧 启用 API 控制...")
    client.enableApiControl(True)
    client.armDisarm(True)
    print("✅ 无人机已解锁")
    
    print("\n🚀 起飞到 5 米高度...")
    client.takeoffAsync().join()
    print("✅ 起飞完成")
    
    # 等待稳定
    time.sleep(3)
    
    # 获取位置
    state = client.getMultirotorState()
    pos = state.kinematics_estimated.position
    altitude = -pos.z_val
    
    print(f"\n📊 当前状态:")
    print(f"   位置: X={pos.x_val:.2f}, Y={pos.y_val:.2f}, Z={pos.z_val:.2f}")
    print(f"   高度: {altitude:.2f} 米")
    
    print("\n🛬 降落...")
    client.landAsync().join()
    print("✅ 降落完成")
    
    # 清理
    client.armDisarm(False)
    client.enableApiControl(False)
    print("\n🎉 测试完成！")

if __name__ == "__main__":
    try:
        simple_takeoff()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n请确保 AirSim 模拟器正在运行！")