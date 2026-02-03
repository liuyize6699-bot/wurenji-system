# QingYu AI Flight Control System - PowerShell Startup Script

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "QingYu AI Flight Control System - PowerShell Start" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting server..." -ForegroundColor Yellow
Write-Host "Service URL: http://localhost:8000" -ForegroundColor White
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Start server
try {
    py simple_server.py
} catch {
    Write-Host "Startup failed: $_" -ForegroundColor Red
    Write-Host "Please make sure Python is installed" -ForegroundColor Yellow
}

Read-Host "Press Enter to exit"