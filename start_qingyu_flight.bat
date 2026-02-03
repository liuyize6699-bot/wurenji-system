@echo off
title QingYu AI Flight Control System
cls
echo.
echo ============================================================
echo        QingYu AI Flight Control System - Quick Start
echo ============================================================
echo.
echo Starting server...
echo Service URL: http://localhost:8000
echo.
echo After startup, you can visit:
echo   System Status: http://localhost:8000/
echo   Airport Info:  http://localhost:8000/airports
echo   Health Check:  http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the service
echo ============================================================
echo.

cd /d "%~dp0"
py simple_server.py

echo.
echo Service stopped
pause