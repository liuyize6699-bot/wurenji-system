@echo off
chcp 65001 >nul
title QingYu AI Flight Control System
echo ============================================================
echo Flight Control System - One-Click Start
echo ============================================================
echo Starting server...
echo.

cd /d "%~dp0"
py simple_server.py

pause