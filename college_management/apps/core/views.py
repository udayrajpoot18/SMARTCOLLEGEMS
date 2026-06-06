from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.http import JsonResponse
from .models import User, Department, Course, AuditLog, Announcement, Event
from .forms import LoginForm, RegisterForm, ProfileUpdateForm, DepartmentForm, CourseForm
from apps.students.models import Student
from apps.teachers.models import Teacher
from apps.attendance.models import Attendance
from apps.fees.models import FeePayment
from apps.examinations.models import Result
from .decorators import role_required, ADMIN_ROLES
import json


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            AuditLog.objects.create(user=user, action='User Login', ip_address=get_client_ip(request))
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        AuditLog.objects.create(user=request.user, action='User Logout', ip_address=get_client_ip(request))
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def register_view(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')
    return render(request, 'core/register.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user
    context = get_dashboard_context(user)
    return render(request, 'core/dashboard.html', context)


def get_dashboard_context(user):
    total_students = Student.objects.filter(is_active=True).count()
    total_teachers = Teacher.objects.filter(is_active=True).count()
    total_departments = Department.objects.count()
    total_courses = Course.objects.filter(is_active=True).count()

    today = timezone.now().date()
    today_attendance = Attendance.objects.filter(date=today)
    present_count = today_attendance.filter(status='present').count()
    total_today = today_attendance.count()
    attendance_pct = round((present_count / total_today * 100), 1) if total_today > 0 else 0

    monthly_fee = FeePayment.objects.filter(
        payment_date__month=today.month,
        payment_date__year=today.year,
        status='paid'
    ).count()

    upcoming_events = Event.objects.filter(event_date__gte=today).order_by('event_date')[:5]
    announcements = Announcement.objects.filter(is_active=True)[:5]
    recent_logs = AuditLog.objects.select_related('user').order_by('-timestamp')[:10]

    monthly_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_att_data = []
    for m in range(1, 13):
        total = Attendance.objects.filter(date__month=m, date__year=today.year).count()
        present = Attendance.objects.filter(date__month=m, date__year=today.year, status='present').count()
        monthly_att_data.append(round(present / total * 100, 1) if total > 0 else 0)

    dept_labels = list(Department.objects.values_list('name', flat=True))
    dept_data = [Student.objects.filter(department__name=d).count() for d in dept_labels]

    return {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
        'total_courses': total_courses,
        'attendance_pct': attendance_pct,
        'monthly_fee': monthly_fee,
        'upcoming_events': upcoming_events,
        'announcements': announcements,
        'recent_logs': recent_logs,
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_att_data': json.dumps(monthly_att_data),
        'dept_labels': json.dumps(dept_labels),
        'dept_data': json.dumps(dept_data),
    }


@login_required
def profile_view(request):
    return render(request, 'core/profile.html', {'user': request.user})


@login_required
def profile_update(request):
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'core/profile_update.html', {'form': form})


@login_required
@role_required(*ADMIN_ROLES)
def settings_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'department':
            form = DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Department added!')
            else:
                messages.error(request, 'Error adding department.')
        elif form_type == 'course':
            form = CourseForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Course added!')
            else:
                messages.error(request, 'Error adding course.')
        return redirect('settings')
    departments = Department.objects.all()
    courses = Course.objects.select_related('department').all()
    dept_form = DepartmentForm()
    course_form = CourseForm()
    return render(request, 'core/settings.html', {
        'departments': departments,
        'courses': courses,
        'dept_form': dept_form,
        'course_form': course_form,
    })


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')
