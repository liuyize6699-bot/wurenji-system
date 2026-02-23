# AirSim 安装指南（Python 3.10+ 兼容方案）

## 🚨 问题说明

AirSim 官方版本主要支持 Python 3.5-3.8，在 Python 3.10+ 上可能遇到兼容性问题。

## 🔧 解决方案

### 方案1：使用虚拟环境（推荐）

#### 步骤1：创建 Python 3.10 虚拟环境

```bash
# 使用 venv 创建虚拟环境
python -m venv airsim_env

# 激活虚拟环境
# Windows:
airsim_env\Scripts\activate

# Linux/Mac:
source airsim_env/bin/activate
```

#### 步骤2：在虚拟环境中安装依赖

```bash
# 升级 pip
python -m pip install --upgrade pip

# 安装兼容的 numpy
pip install "numpy>=1.21.0,<2.0.0"

# 尝试安装 airsim
pip install airsim

# 如果失败，尝试从源码安装
pip install git+https://github.com/microsoft/AirSim.git#subdirectory=PythonClient
```

#### 步骤3：安装其他依赖

```bash
pip install -r requirements_airsim.txt
```

#### 步骤4：退出虚拟环境

```bash
deactivate
```

### 方案2：使用 conda 环境

```bash
# 创建 Python 3.10 的 conda 环境
conda create -n airsim_env python=3.10

# 激活环境
conda activate airsim_env

# 安装依赖
pip install airsim numpy opencv-python

# 退出环境
conda deactivate
```

### 方案3：使用 pyenv（多版本管理）

```bash
# 安装 pyenv（如果还没有）
# Windows: 使用 pyenv-win
# Linux/Mac: curl https://pyenv.run | bash

# 安装 Python 3.10
pyenv install 3.10.11

# 为项目设置 Python 3.10
pyenv local 3.10.11

# 创建虚拟环境
python -m venv venv

# 激活并安装
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install airsim numpy
```

## 📦 兼容性配置

### 创建 .python-version 文件（pyenv）

```bash
echo "3.10.11" > .python-version
```

### 创建虚拟环境启动脚本

**Windows (activate_airsim.bat):**
```batch
@echo off
call airsim_env\Scripts\activate.bat
echo AirSim 环境已激活 (Python 3.10)
```

**Linux/Mac (activate_airsim.sh):**
```bash
#!/bin/bash
source airsim_env/bin/activate
echo "AirSim 环境已激活 (Python 3.10)"
```

## 🧪 验证安装

创建测试文件 `test_airsim_install.py`:

```python
#!/usr/bin/env python3
import sys
print(f"Python 版本: {sys.version}")

try:
    import numpy as np
    print(f"✅ NumPy 版本: {np.__version__}")
except ImportError as e:
    print(f"❌ NumPy 导入失败: {e}")

try:
    import airsim
    print(f"✅ AirSim 版本: {airsim.__version__ if hasattr(airsim, '__version__') else '已安装'}")
except ImportError as e:
    print(f"❌ AirSim 导入失败: {e}")

try:
    import cv2
    print(f"✅ OpenCV 版本: {cv2.__version__}")
except ImportError as e:
    print(f"❌ OpenCV 导入失败: {e}")
```

运行测试：
```bash
python test_airsim_install.py
```

## 🔄 在项目中使用

### 方法1：每次手动激活

```bash
# 激活虚拟环境
airsim_env\Scripts\activate  # Windows
source airsim_env/bin/activate  # Linux/Mac

# 运行你的脚本
python your_script.py

# 退出
deactivate
```

### 方法2：使用脚本自动激活

创建 `run_with_airsim.bat` (Windows):
```batch
@echo off
call airsim_env\Scripts\activate.bat
python %*
call deactivate
```

使用：
```bash
run_with_airsim.bat your_script.py
```

### 方法3：在代码中指定解释器

在脚本开头添加 shebang：
```python
#!/path/to/airsim_env/bin/python
```

## 🚀 替代方案：使用 Docker

如果虚拟环境方案不理想，可以使用 Docker：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements_airsim.txt .
RUN pip install -r requirements_airsim.txt

COPY . .

CMD ["python", "your_script.py"]
```

## 📝 注意事项

1. **全局 Python 版本不受影响**：虚拟环境是独立的，不会改变系统的 Python 3.14
2. **项目隔离**：每个项目可以有自己的虚拟环境和依赖版本
3. **AirSim 限制**：如果 AirSim 完全不兼容 Python 3.10+，考虑使用替代库或降级到 Python 3.8

## 🔗 相关资源

- AirSim GitHub: https://github.com/microsoft/AirSim
- AirSim Python API: https://microsoft.github.io/AirSim/apis/
- Python 虚拟环境文档: https://docs.python.org/3/library/venv.html