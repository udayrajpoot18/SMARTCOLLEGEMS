#!/bin/bash
echo "========================================"
echo " Smart College Management System Setup"
echo "========================================"

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cd college_management
python ../manage.py makemigrations core students teachers attendance examinations assignments fees library notices
python ../manage.py migrate
python ../manage.py create_sample_data

echo "========================================"
echo " Open: http://localhost:8000"
echo " Login: admin / admin123"
echo "========================================"

python ../manage.py runserver
