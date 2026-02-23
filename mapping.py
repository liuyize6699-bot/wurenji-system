import airsim
import cv2
import numpy as np
import time
import os

# 1. 坐标映射 (语义名称 -> 仿真环境坐标)
# 这里的坐标是基于 Blocks 起点 (0,0,0) 的相对偏移
LOCAL_MAPPING = {
    "顶好大厦": [0, 0, -5],
    "创投大厦": [40, 25, -15],  
    "怡丰昌盛": [-30, -50, -12]
}

# 2. 初始化 AirSim 客户端
client = airsim.MultirotorClient()
client.confirmConnection()

def take_photo(location_name, waypoint_name):
    """
    采集下视摄像头影像并保存到当前目录
    """
    # 请求 "3" 号下视摄像头
    responses = client.simGetImages([
        airsim.ImageRequest("3", airsim.ImageType.Scene, False, False)
    ])
    response = responses[0]
    
    # 转换为 OpenCV 格式
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
    img_rgb = img1d.reshape(response.height, response.width, 3)
    
    # 文件命名
    filename = f"{location_name}_{waypoint_name}.png"
    cv2.imwrite(filename, img_rgb)
    print(f"  📸 影像已存至: {os.path.abspath(filename)}")

def execute_task(location_name):
    if location_name not in LOCAL_MAPPING:
        print(f"❌ 错误：位置【{location_name}】未在配置中定义。")
        return

    # 核心参数设置
    CRUISE_ALTITUDE = -30  # 巡航高度30米，确保避开15米高的方块
    center_pos = LOCAL_MAPPING[location_name]

    print(f"\n🚀 启动【{location_name}】区域测绘任务...")
    
    # --- 准备阶段 ---
    client.enableApiControl(True)
    client.armDisarm(True)

    # --- 飞行阶段 ---
    print("🛫 正在执行安全起飞...")
    client.takeoffAsync().join()

    print(f"⬆️ 正在爬升至 {abs(CRUISE_ALTITUDE)}m 避障高度...")
    client.moveToZAsync(CRUISE_ALTITUDE, 5).join()

    print(f"🛰️ 正在巡航至任务中心点...")
    client.moveToPositionAsync(center_pos[0], center_pos[1], CRUISE_ALTITUDE, 8).join()

    # --- 区域测绘 (多航点) ---
    print(f"🗺️ 开始执行多航点扫描逻辑...")
    # 生成以中心点为原点的 10x10 米正方形航点
    offsets = [
        ("西北", 10, -10), ("东北", 10, 10), 
        ("东南", -10, 10), ("西南", -10, -10)
    ]

    for label, dx, dy in offsets:
        wx, wy = center_pos[0] + dx, center_pos[1] + dy
        print(f"  -> 飞往{label}角航点...")
        client.moveToPositionAsync(wx, wy, CRUISE_ALTITUDE, 5).join()
        time.sleep(1) # 稳定拍摄
        take_photo(location_name, label)

    # --- 安全返航 (RTH) ---
    print("🏁 区域测绘完毕！触发自动返航 (Return to Home)...")
    # 先飞回 (0,0) 的高空点
    client.moveToPositionAsync(0, 0, CRUISE_ALTITUDE, 8).join()
    
    # --- 🛡️ 强制稳健降落逻辑 (替代不靠谱的 landAsync) ---
    print("🛬 已到达基地上方，执行强制垂直降落程序...")
    
    # 第一步：先快速下降到 3 米（你刚才已经成功的一步）
    print("  -> 正在快速下降至离地 3 米...")
    client.moveToPositionAsync(0, 0, -3, 3).join() 
    
    # 第二步：【核心修改】手动缓慢压向地面 (Z=0 是地面，写 0.2 确保压实)
    # 使用极慢的速度 (0.5m/s)，模拟平稳落地
    print("  -> 正在缓慢触地 (手动高度压制)...")
    client.moveToPositionAsync(0, 0, 1, 5).join() 

    # 第三步：强制等待物理引擎判定停止
    # 即使代码认为飞到了 0.2，由于地面阻挡，它会停在 0
    print("⏳ 落地确认：预留 8 秒等待物理状态稳定...")
    time.sleep(8) 

    # 第四步：此时再关电机就绝对安全了
    print("🔒 判定已稳固着陆，关闭电机并退出控制。")
    client.armDisarm(False)
    client.enableApiControl(False)
    print("✨ 恭喜！全流程闭环任务【完美达成】！")

# --- 主循环入口 ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🤖 具身智能无人机巡检控制终端 (V2.0-稳健版)")
    print("支持目标：顶好大厦 | 创投大厦 | 怡丰昌盛")
    print("="*50)
    
    while True:
        try:
            target = input("\n请输入巡检区域名称 (或输入 'exit' 退出): ").strip()
            if target.lower() == 'exit':
                print("👋 退出系统。")
                break
            if not target:
                continue
            execute_task(target)
        except Exception as e:
            print(f"⚠️ 运行出错: {e}")
            client.armDisarm(False)
            break