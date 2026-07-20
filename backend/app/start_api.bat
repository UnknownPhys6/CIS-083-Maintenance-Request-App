@echo off

cd /d "%~dp0"

echo Starting Maintenance Request Backend...
echo.

call .venv\Scripts\activate

start "Backend" cmd /k python -m uvicorn api:app --reload
start "ngrok api access" cmd /k ngrok http 8000
start "ngrok sql access" cmd /k ngrok tcp 3306

echo.
echo Backend stopped.
pause
