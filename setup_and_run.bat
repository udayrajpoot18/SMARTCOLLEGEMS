@echo off
echo.
echo ========================================
echo  Smart College Management System Setup
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [2/5] Installing dependencies...
pip install -r requirements.txt

echo [3/5] Running database migrations...
python manage.py makemigrations core students teachers attendance examinations assignments fees library notices
python manage.py migrate

echo [4/5] Creating sample data...
python manage.py create_sample_data

echo [5/5] Starting development server...
echo.
echo ========================================
echo  Open: http://localhost:8000
echo  Admin: http://localhost:8000/admin/
echo.
echo  Demo Credentials:
echo    admin      / admin123
echo    principal1 / principal123
echo    teacher1   / teacher123
echo    student1   / student123
echo ========================================
echo.
python manage.py runserver

pause
