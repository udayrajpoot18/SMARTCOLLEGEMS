# 🎓 Smart College Management System

A complete, production-ready College Management System built with **Python Django** featuring a premium modern UI with glassmorphism effects, dark mode, and full CRUD operations.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python Django 4.2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML5, CSS3, JavaScript (ES6+) |
| UI Framework | Bootstrap 5.3 |
| Charts | Chart.js 4.4 |
| Auth | Django Authentication System |
| API | Django REST Framework |
| Fonts | Google Fonts (Inter) |
| Icons | Bootstrap Icons |

---

## ✨ Features

### 🎨 UI/UX
- Glassmorphism card effects with backdrop blur
- Gradient backgrounds & animated sidebar
- Dark Mode / Light Mode toggle (persisted in localStorage)
- Smooth CSS animations & AOS-style scroll animations
- Animated counter stats on dashboard
- Toast notifications
- Responsive mobile-first design
- Loading screen with spinner

### 👥 User Roles
- **Super Admin** - Full system control
- **Principal** - Analytics, leave approvals, notices
- **Teacher** - Attendance, assignments, marks, materials
- **Student** - View profile, results, assignments, fees
- **Parent** - Track attendance, results, fee status

### 📚 Core Modules
1. **Dashboard** - Stats, charts, events, activity log
2. **Student Management** - CRUD, profiles, ID cards, promotion
3. **Teacher Management** - CRUD, profiles, subject allocation
4. **Attendance** - Daily marking, reports, analytics
5. **Examinations** - Exam creation, mark entry, GPA/CGPA
6. **Assignments** - Create, submit, track status
7. **Study Materials** - Upload PDF/PPT/Video links
8. **Fee Management** - Structures, payments, receipts
9. **Library** - Books, issue/return, fine calculation
10. **Notices** - Priority notices, announcements
11. **Leave Management** - Apply, approve/reject workflow
12. **Settings** - Departments, courses management
13. **Audit Logs** - Activity tracking

### 🔌 REST API
- Full REST API via Django REST Framework
- Endpoints for Users, Departments, Courses
- Session-based authentication

---

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- pip

### Quick Setup

```bash
# 1. Navigate to project
cd SmartCollegeMS

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create sample data (includes demo accounts)
python manage.py create_sample_data

# 7. Start development server
python manage.py runserver
```

Open browser: **http://localhost:8000**

---

## 🔑 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Super Admin | `admin` | `admin123` |
| Principal | `principal1` | `principal123` |
| Teacher | `teacher1` | `teacher123` |
| Student | `student1` | `student123` |

---

## 📁 Project Structure

```
SmartCollegeMS/
├── manage.py
├── requirements.txt
├── README.md
├── college_management/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── apps/
│   │   ├── core/         # Users, Departments, Courses, Auth
│   │   ├── students/     # Student Management
│   │   ├── teachers/     # Teacher Management
│   │   ├── attendance/   # Attendance Tracking
│   │   ├── examinations/ # Exams, Results, GPA
│   │   ├── assignments/  # Assignments, Study Materials
│   │   ├── fees/         # Fee Management
│   │   ├── library/      # Library System
│   │   └── notices/      # Notices, Leave Management
│   ├── templates/        # HTML Templates
│   ├── static/
│   │   ├── css/style.css # Premium UI styles
│   │   └── js/main.js    # Frontend JS
│   └── media/            # Uploaded files
```

---

## 🌐 REST API Endpoints

```
GET/POST    /api/users/
GET/PUT/DEL /api/users/{id}/
GET/POST    /api/departments/
GET/POST    /api/courses/
```

---

## 🚀 Deployment (Production)

### Environment Variables (.env)
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgres://user:pass@host:5432/dbname
```

### PostgreSQL Setup
In `settings.py`, replace the DATABASES config:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'college_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Deployment Commands
```bash
python manage.py collectstatic
gunicorn college_management.wsgi:application
```

---

## 📊 Database Schema

### Core Models
- **User** (extends AbstractUser) - role, phone, profile_photo, dob
- **Department** - name, code, hod, established_year
- **Course** - name, code, dept, credits, semester
- **AuditLog** - user, action, ip_address, timestamp

### Academic Models
- **Student** - enrollment, personal info, parent info, photo
- **Teacher** - employee_id, designation, subjects (M2M)
- **Attendance** - student, course, date, status
- **Exam** - name, type, course, marks, date
- **Result** - student, exam, marks, grade (auto-calculated), GPA

### Support Models
- **Assignment** / **Submission** / **StudyMaterial**
- **FeeStructure** / **FeePayment**
- **Book** / **BookIssue**
- **Notice** / **LeaveRequest**
- **Announcement** / **Event**

---

## 🎯 Grade System (Automatic)

| Marks % | Grade | Points |
|---------|-------|--------|
| ≥ 90% | O | 10.0 |
| ≥ 80% | A+ | 9.0 |
| ≥ 70% | A | 8.0 |
| ≥ 60% | B+ | 7.0 |
| ≥ 50% | B | 6.0 |
| ≥ 40% | C | 5.0 |
| < 40% | F | 0.0 |

---

## 📝 License

MIT License - Free for academic and commercial use.

---

## 🙏 Credits

Built as a Final Year B.Tech Major Project using Django, Bootstrap 5, and Chart.js.
