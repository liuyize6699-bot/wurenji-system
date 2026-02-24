import requests
import time
from mapping import execute_task 

# 这里的 URL 必须对应你 main.py 里的 get 接口
URL = "https://wurenji.zeabur.app/get_task"

print("📡 [本地端] 监听程序已启动，等待云端指挥...")

while True:
    try:
        r = requests.get(URL, timeout=5)
        data = r.json()
        
        # 拿到任务地名（如：顶好大厦）
        target_location = data.get("location")
        
        if target_location:
            print(f"🚀 收到云端调度指令：前往 [{target_location}]")
            execute_task(target_location)
            print("🏁 任务执行完毕，继续监听...")
            
    except Exception as e:
        # 保持安静，每2秒检查一次
        pass
    time.sleep(2)
