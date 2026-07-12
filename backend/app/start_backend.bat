@echo off

cd /d "%~dp0"

echo Starting Maintenance Request Backend...
echo.

call .venv\Scripts\activate

python -m uvicorn api:app --reload

echo.
echo Backend stopped.
pause
