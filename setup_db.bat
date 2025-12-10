@echo off
echo ==========================================
echo Antrodia Project - Database Setup Script
echo ==========================================

REM Ensure we are in the script directory
cd /d "%~dp0"

echo [1/4] Cleaning up potential conflicts...
if exist db.sqlite3 (
    del db.sqlite3
    echo - Deleted old database.
)

echo.
echo [2/4] Creating migrations for apps...
python manage.py makemigrations home products research
python manage.py makemigrations

echo.
echo [3/4] Applying database migrations...
echo (This might take a few seconds)
python manage.py migrate

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Migration failed! Please check the output above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [4/5] Loading Demo Data...
python manage.py load_demo_data

echo.
echo [5/5] Setup Complete!
echo.
echo Please create your admin account now:
python manage.py createsuperuser

echo.
echo ==========================================
echo All done. You can now run: python manage.py runserver
echo ==========================================
pause
