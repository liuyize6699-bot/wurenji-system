#!/usr/bin/env python3
"""
轻语AI飞控指挥系统 - Zeabur部署入口文件
"""

import os
import uvicorn
from main import app

if __name__ == "__main__":
    # 从环境变量获取端口，默认8080（Zeabur常用端口）
    port = int(os.environ.get("PORT", 8080))
    
    # 启动FastAPI应用
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )