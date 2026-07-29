@echo off
cd /d "%~dp0"

echo Starting Maintenance Request Backend...
echo.

call "%~dp0..\..\.venv\Scripts\python.exe" -m uvicorn api:app --reload

pause
