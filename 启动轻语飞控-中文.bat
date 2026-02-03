@echo off
chcp 65001 >nul
title 轻语AI飞控指挥系统
cls
echo.
echo ============================================================
echo           轻语AI飞控指挥系统 - 一键启动
echo ============================================================
echo.
echo 正在启动服务器...
echo 服务地址: http://localhost:8000
echo.
echo 启动后可以访问:
echo   系统状态: http://localhost:8000/
echo   机场信息: http://localhost:8000/airports
echo   健康检查: http://localhost:8000/health
echo.
echo 按 Ctrl+C 可以停止服务
echo ============================================================
echo.

cd /d "%~dp0"
py simple_server.py

echo.
echo 服务已停止
pause