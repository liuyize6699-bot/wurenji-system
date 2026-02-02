#!/usr/bin/env python3
"""
福华创新AI飞控指挥系统 - 启动脚本
"""

import uvicorn
import sys
import os

def main():
    """启动服务"""
    print("=" * 60)
    print("🚁 福华创新AI飞控指挥系统")
    print("=" * 60)
    print("🌐 服务地址: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()