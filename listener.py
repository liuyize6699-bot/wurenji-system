import requests
import time
from mapping import execute_task 

# 你的 Zeabur 域名
URL = "https://wurenji-system.zeabur.app/get_task"

while True:
    try:
        r = requests.get(URL, timeout=5)
        data = r.json()
        if data.get("location"):
            print(f"收到任务: {data['location']}")
            execute_task(data['location'])
    except Exception as e:
        # 保持静默监听
        pass
    time.sleep(2)
