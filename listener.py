import requests
import time
# 导入你刚才写好的那个稳健版执行函数
from mapping import execute_task 

ZEABUR_URL = "https://wurenji.zeabur.app/get_task"

print("📡 无人机‘监听模式’已启动，正在等待云端指令...")

while True:
    try:
        # 1. 询问信箱：有没有新任务？
        response = requests.get(ZEABUR_URL)
        task_data = response.json()
        target_name = task_data.get("target")

        if target_name:
            print(f"🔔 收到云端紧急指令！目的地：{target_name}")
            # 2. 触发你之前写好的那一整套：起飞、爬升、测绘、返航
            execute_task(target_name)
            print("🏁 任务完成，继续监听...")
        
    except Exception as e:
        print(f"⚠️ 网络连接异常: {e}")
    
    # 3. 每隔 2 秒检查一次，防止请求太快被服务器封禁
    time.sleep(2)