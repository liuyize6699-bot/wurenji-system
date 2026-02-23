import airsim
import cv2
import numpy as np
import os
import time

print("📡 正在连接 AirSim 模拟器...")
client = airsim.MultirotorClient()
client.confirmConnection()

# 获取控制权并解锁无人机
client.enableApiControl(True)
client.armDisarm(True)

print("🚁 螺旋桨启动，准备起飞...")
client.takeoffAsync().join()

# 飞高一点，视野更好 (注意：AirSim 的坐标系里，Z轴向下为正，向上为负，所以 -5 表示向上飞5米)
print("🚀 正在爬升至 5 米高空...")
client.moveToPositionAsync(0, 0, -5, 2).join() 
time.sleep(2) # 悬停 2 秒钟让机身稳定

print("📸 咔嚓！正在调用前置摄像头拍照...")
# "0" 代表前置摄像头，ImageType.Scene 代表获取真实的彩色画面
responses = client.simGetImages([
    airsim.ImageRequest("3", airsim.ImageType.Scene, False, False)
])
response = responses[0]

print("🧠 正在使用 NumPy 和 OpenCV 处理图像数据...")
# 这就是你装好的 NumPy 在干活：把原始字节流变成一维数组
img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
# 把一维数组重塑成二维的彩色图片长宽矩阵 (高, 宽, 3个颜色通道)
img_rgb = img1d.reshape(response.height, response.width, 3)

# 保存图片到当前文件夹
filename = "my_first_aerial_photo.png"
cv2.imwrite(filename, img_rgb)
print(f"✅ 照片洗出来了！已保存为: {filename}")

print("🛬 任务完成，正在自动降落...")
client.landAsync().join()

# 锁死电机，归还控制权
client.armDisarm(False)
client.enableApiControl(False)
print("🎉 完美收工！赶快去文件夹里看看你拍的照片吧！")