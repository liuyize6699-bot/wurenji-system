@echo off
echo ============================================================
echo 创建 AirSim 虚拟环境 (Python 3.10)
echo ============================================================
echo.

REM 检查是否已存在虚拟环境
if exist airsim_env (
    echo 虚拟环境已存在，跳过创建
) else (
    echo 正在创建虚拟环境...
    python -m venv airsim_env
    if errorlevel 1 (
        echo 错误: 无法创建虚拟环境
        echo 请确保已安装 Python 3.10
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功
)

echo.
echo 激活虚拟环境...
call airsim_env\Scripts\activate.bat

echo.
echo 升级 pip...
python -m pip install --upgrade pip

echo.
echo 安装依赖...
pip install -r requirements_airsim.txt

echo.
echo 尝试安装 AirSim...
pip install airsim
if errorlevel 1 (
    echo.
    echo AirSim 安装失败，尝试从源码安装...
    pip install git+https://github.com/microsoft/AirSim.git#subdirectory=PythonClient
)

echo.
echo ============================================================
echo 安装完成！
echo ============================================================
echo.
echo 使用方法:
echo 1. 激活环境: airsim_env\Scripts\activate
echo 2. 运行脚本: python your_script.py
echo 3. 退出环境: deactivate
echo.
pause