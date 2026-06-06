from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import Attendance
from .forms import AttendanceForm, BulkAttendanceForm
from apps.students.models import Student
from apps.core.models import Course, Department
from apps.core.decorators import role_required, ADMIN_ROLES, TEACHER_ROLES, ALL_ROLES
import json


@login_required
@role_required(*ALL_ROLES)
def attendance_dashboard(request):
    today = timezone.now().date()
    today_records = Attendance.objects.filter(date=today)
    present = today_records.filter(status='present').count()
    absent = today_records.filter(status='absent').count()
    total = today_records.count()
    pct = round(present / total * 100, 1) if total > 0 else 0

    last_7_days = []
    for i in range(6, -1, -1):
        from datetime import timedelta
        d = today - timedelta(days=i)
        t = Attendance.objects.filter(date=d).count()
        p = Attendance.objects.filter(date=d, status='present').count()
        last_7_days.append({'date': d.strftime('%a'), 'pct': round(p / t * 100, 1) if t > 0 else 0})

    return render(request, 'attendance/dashboard.html', {
        'present': present, 'absent': absent, 'total': total, 'pct': pct,
        'last_7_days': json.dumps(last_7_days),
        'today': today,
    })


@login_required
@role_required(*TEACHER_ROLES)
def take_attendance(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, pk=course_id)
        students = Student.objects.filter(department=course.department, semester=course.semester, is_active=True)
        created = 0
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'absent')
            Attendance.objects.update_or_create(
                student=student, course=course, date=date,
                defaults={'status': status}
            )
            created += 1
        messages.success(request, f'Attendance recorded for {created} students.')
        return redirect('attendance_dashboard')

    courses = Course.objects.filter(is_active=True)
    return render(request, 'attendance/take_attendance.html', {
        'courses': courses, 'today': timezone.now().date()
    })


@login_required
@role_required(*TEACHER_ROLES)
def get_students_for_course(request):
    course_id = request.GET.get('course_id')
    course = get_object_or_404(Course, pk=course_id)
    students = list(Student.objects.filter(
        department=course.department, semester=course.semester, is_active=True
    ).values('id', 'first_name', 'last_name', 'enrollment_number'))
    from django.http import JsonResponse
    return JsonResponse({'students': students})


@login_required
@role_required(*ALL_ROLES)
def attendance_report(request):
    dept_filter = request.GET.get('dept', '')
    course_filter = request.GET.get('course', '')
    month = int(request.GET.get('month', timezone.now().month))
    year = int(request.GET.get('year', timezone.now().year))

    records = Attendance.objects.select_related('student', 'course').filter(
        date__month=month, date__year=year
    )
    if dept_filter:
        records = records.filter(student__department_id=dept_filter)
    if course_filter:
        records = records.filter(course_id=course_filter)

    student_summary = {}
    for r in records:
        sid = r.student.id
        if sid not in student_summary:
            student_summary[sid] = {'student': r.student, 'total': 0, 'present': 0}
        student_summary[sid]['total'] += 1
        if r.status == 'present':
            student_summary[sid]['present'] += 1

    for sid in student_summary:
        t = student_summary[sid]['total']
        p = student_summary[sid]['present']
        student_summary[sid]['pct'] = round(p / t * 100, 1) if t > 0 else 0

    months = [
        (1,'January'),(2,'February'),(3,'March'),(4,'April'),
        (5,'May'),(6,'June'),(7,'July'),(8,'August'),
        (9,'September'),(10,'October'),(11,'November'),(12,'December'),
    ]

    return render(request, 'attendance/report.html', {
        'student_summary': student_summary.values(),
        'departments': Department.objects.all(),
        'courses': Course.objects.all(),
        'month': month, 'year': year,
        'months': months,
        'dept_filter': dept_filter, 'course_filter': course_filter,
    })


@login_required
@role_required(*ALL_ROLES)
def student_attendance_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    records = Attendance.objects.filter(student=student).select_related('course').order_by('-date')
    total = records.count()
    present = records.filter(status='present').count()
    pct = round(present / total * 100, 1) if total > 0 else 0
    return render(request, 'attendance/student_detail.html', {
        'student': student, 'records': records, 'total': total, 'present': present, 'pct': pct
    })
