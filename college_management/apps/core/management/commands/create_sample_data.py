from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Creates sample data for the College Management System'

    def handle(self, *args, **kwargs):
        from apps.core.models import User, Department, Course, Announcement, Event
        from apps.students.models import Student
        from apps.teachers.models import Teacher
        from apps.attendance.models import Attendance
        from apps.examinations.models import Exam, Result
        from apps.fees.models import FeeStructure, FeePayment
        from apps.library.models import Book
        from apps.notices.models import Notice

        self.stdout.write('Creating sample data...')

        # Super Admin
        admin, _ = User.objects.get_or_create(username='admin', defaults={
            'first_name': 'System', 'last_name': 'Admin',
            'email': 'admin@college.edu', 'role': 'super_admin',
            'is_staff': True, 'is_superuser': True,
        })
        admin.set_password('admin123')
        admin.save()

        # Principal
        principal, _ = User.objects.get_or_create(username='principal1', defaults={
            'first_name': 'Dr. Rajesh', 'last_name': 'Kumar',
            'email': 'principal@college.edu', 'role': 'principal',
        })
        principal.set_password('principal123')
        principal.save()

        # Departments
        dept_data = [
            ('Computer Science & Engineering', 'CSE'),
            ('Electronics & Communication', 'ECE'),
            ('Mechanical Engineering', 'ME'),
            ('Civil Engineering', 'CE'),
            ('Information Technology', 'IT'),
        ]
        departments = []
        for name, code in dept_data:
            d, _ = Department.objects.get_or_create(code=code, defaults={'name': name, 'established_year': 2005})
            departments.append(d)

        # Courses
        course_data = [
            ('Data Structures', 'CS101', departments[0], 3, 1),
            ('Algorithms', 'CS102', departments[0], 4, 2),
            ('Database Systems', 'CS201', departments[0], 3, 3),
            ('Machine Learning', 'CS301', departments[0], 4, 5),
            ('Digital Electronics', 'EC101', departments[1], 3, 1),
            ('Signals & Systems', 'EC201', departments[1], 4, 3),
            ('Thermodynamics', 'ME101', departments[2], 3, 1),
            ('Fluid Mechanics', 'ME201', departments[2], 3, 3),
        ]
        courses = []
        for name, code, dept, credits, sem in course_data:
            c, _ = Course.objects.get_or_create(code=code, defaults={
                'name': name, 'department': dept, 'credits': credits, 'semester': sem
            })
            courses.append(c)

        # Teachers
        teacher_data = [
            ('Priya', 'Sharma', 'EMP001', 'priya@college.edu', departments[0], 'assistant_professor', 'teacher1'),
            ('Arjun', 'Patel', 'EMP002', 'arjun@college.edu', departments[0], 'associate_professor', 'teacher2'),
            ('Meena', 'Reddy', 'EMP003', 'meena@college.edu', departments[1], 'professor', 'teacher3'),
            ('Suresh', 'Rao', 'EMP004', 'suresh@college.edu', departments[2], 'assistant_professor', 'teacher4'),
            ('Lakshmi', 'Iyer', 'EMP005', 'lakshmi@college.edu', departments[3], 'lecturer', 'teacher5'),
        ]
        teachers = []
        for fn, ln, eid, email, dept, desig, uname in teacher_data:
            t_user, _ = User.objects.get_or_create(username=uname, defaults={
                'first_name': fn, 'last_name': ln, 'email': email, 'role': 'teacher'
            })
            t_user.set_password('teacher123')
            t_user.save()
            t, _ = Teacher.objects.get_or_create(employee_id=eid, defaults={
                'user': t_user, 'first_name': fn, 'last_name': ln, 'email': email,
                'phone': f'98{random.randint(10000000, 99999999)}',
                'department': dept, 'designation': desig,
                'qualification': 'M.Tech', 'experience_years': random.randint(2, 15),
                'joining_date': date(2015, 6, 1),
            })
            teachers.append(t)

        # Students
        student_names = [
            ('Amit', 'Singh'), ('Priti', 'Verma'), ('Rohan', 'Gupta'), ('Sneha', 'Joshi'),
            ('Kiran', 'Nair'), ('Rahul', 'Mishra'), ('Anjali', 'Tiwari'), ('Vijay', 'Kumar'),
            ('Neha', 'Shah'), ('Arun', 'Pillai'), ('Divya', 'Menon'), ('Ravi', 'Chandra'),
        ]
        students = []
        for i, (fn, ln) in enumerate(student_names):
            enroll = f'CS{2021 + (i // 4):4d}{(i % 100) + 1:03d}'
            dept = departments[i % 3]
            sem = (i % 4) + 1
            s_user, _ = User.objects.get_or_create(username=f'student{i+1}', defaults={
                'first_name': fn, 'last_name': ln, 'email': f's{i+1}@college.edu', 'role': 'student'
            })
            s_user.set_password('student123')
            s_user.save()
            s, _ = Student.objects.get_or_create(enrollment_number=enroll, defaults={
                'user': s_user, 'first_name': fn, 'last_name': ln,
                'email': f's{i+1}@college.edu', 'phone': f'97{random.randint(10000000, 99999999)}',
                'gender': 'M' if i % 2 == 0 else 'F', 'date_of_birth': date(2002, (i % 12) + 1, 15),
                'department': dept, 'semester': sem,
                'address': f'{100+i} Main Street, Bangalore', 'parent_name': f'Parent of {fn}',
                'parent_phone': f'96{random.randint(10000000, 99999999)}',
                'admission_date': date(2021, 7, 15),
            })
            students.append(s)

        # Attendance
        today = date.today()
        for student in students[:8]:
            for dept_course in courses[:4]:
                if dept_course.department == student.department or dept_course.semester == student.semester:
                    for days_ago in range(30):
                        att_date = today - timedelta(days=days_ago)
                        if att_date.weekday() < 5:
                            Attendance.objects.get_or_create(
                                student=student, course=dept_course, date=att_date,
                                defaults={'status': 'present' if random.random() > 0.2 else 'absent'}
                            )

        # Exams & Results
        for c in courses[:4]:
            exam, _ = Exam.objects.get_or_create(
                name=f'Mid Semester - {c.code}', course=c,
                defaults={'exam_type': 'mid_term', 'total_marks': 50, 'passing_marks': 20,
                          'exam_date': today - timedelta(days=15), 'semester': c.semester}
            )
            for s in students[:6]:
                if s.department == c.department or True:
                    Result.objects.get_or_create(student=s, exam=exam, defaults={
                        'marks_obtained': random.randint(20, 50)
                    })

        # Fee Structures
        for dept in departments[:3]:
            for sem in range(1, 5):
                FeeStructure.objects.get_or_create(
                    name=f'{dept.code} Sem {sem} Fees', department=dept, semester=sem,
                    defaults={'tuition_fee': 45000, 'exam_fee': 2000, 'library_fee': 500, 'other_fee': 1000}
                )

        # Fee Payments
        import uuid
        for s in students[:6]:
            FeePayment.objects.get_or_create(
                student=s, transaction_id=f'TXN{uuid.uuid4().hex[:10].upper()}',
                defaults={
                    'amount_paid': 48500, 'payment_date': today - timedelta(days=random.randint(5, 60)),
                    'payment_method': random.choice(['online', 'cash', 'dd']),
                    'status': 'paid',
                }
            )

        # Books
        book_data = [
            ('Introduction to Algorithms', 'CLRS', '978-0262033848', 'textbook'),
            ('Clean Code', 'Robert C. Martin', '978-0132350884', 'reference'),
            ('The Pragmatic Programmer', 'Hunt & Thomas', '978-0135957059', 'reference'),
            ('Database System Concepts', 'Silberschatz', '978-0078022159', 'textbook'),
            ('Computer Networks', 'Andrew Tanenbaum', '978-0132126953', 'textbook'),
        ]
        for title, author, isbn, cat in book_data:
            Book.objects.get_or_create(isbn=isbn, defaults={
                'title': title, 'author': author, 'category': cat,
                'total_copies': random.randint(3, 10), 'available_copies': random.randint(1, 5),
                'rack_number': f'R{random.randint(1,10)}'
            })

        # Announcements
        Announcement.objects.get_or_create(
            title='Welcome to New Semester!',
            defaults={'content': 'Welcome to the new academic semester. Classes begin from Monday.', 'target': 'all', 'created_by': admin}
        )
        Announcement.objects.get_or_create(
            title='Examination Schedule Released',
            defaults={'content': 'The mid-semester examination schedule has been released. Check the notice board.', 'target': 'students', 'created_by': principal}
        )

        # Events
        Event.objects.get_or_create(
            title='Annual Tech Fest',
            defaults={'description': 'Annual technology festival with competitions and workshops.',
                      'event_date': today + timedelta(days=15), 'venue': 'Main Auditorium', 'created_by': admin}
        )
        Event.objects.get_or_create(
            title='Sports Day',
            defaults={'description': 'Annual sports day with various indoor and outdoor events.',
                      'event_date': today + timedelta(days=30), 'venue': 'College Ground', 'created_by': admin}
        )

        # Notices
        Notice.objects.get_or_create(
            title='Library Timings Changed',
            defaults={'content': 'Library will now be open from 8 AM to 9 PM on all working days.',
                      'target': 'all', 'priority': 'medium', 'created_by': admin}
        )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('Demo Login Credentials:'))
        self.stdout.write(self.style.SUCCESS('  Admin:     admin / admin123'))
        self.stdout.write(self.style.SUCCESS('  Principal: principal1 / principal123'))
        self.stdout.write(self.style.SUCCESS('  Teacher:   teacher1 / teacher123'))
        self.stdout.write(self.style.SUCCESS('  Student:   student1 / student123'))
