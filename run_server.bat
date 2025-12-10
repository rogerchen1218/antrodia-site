@echo off
echo Starting Antrodia Web Server...
cd /d "%~dp0"

REM Open the browser after a short delay (to let server start)
timeout /t 3 >nul
start http://127.0.0.1:8000/
start http://127.0.0.1:8000/admin/

echo Server is running. Press CTRL+C to stop.
echo.
python manage.py runserver
pause
