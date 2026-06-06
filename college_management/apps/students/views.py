from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from .models import Student
from .forms import StudentForm
from apps.core.models import Department
from apps.core.decorators import role_required, ADMIN_ROLES, TEACHER_ROLES, ALL_ROLES
import io


@login_required
@role_required(*ALL_ROLES)
def student_list(request):
    query = request.GET.get('q', '')
    dept_filter = request.GET.get('dept', '')
    sem_filter = request.GET.get('sem', '')
    students = Student.objects.select_related('department').filter(is_active=True)
    if query:
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(enrollment_number__icontains=query) | Q(email__icontains=query)
        )
    if dept_filter:
        students = students.filter(department_id=dept_filter)
    if sem_filter:
        students = students.filter(semester=sem_filter)
    paginator = Paginator(students, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    departments = Department.objects.all()
    return render(request, 'students/student_list.html', {
        'page_obj': page_obj,
        'departments': departments,
        'query': query,
        'dept_filter': dept_filter,
        'sem_filter': sem_filter,
        'total': students.count(),
    })


@login_required
@role_required(*ADMIN_ROLES)
def student_add(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student added successfully!')
        return redirect('student_list')
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})


@login_required
@role_required(*ADMIN_ROLES)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('student_detail', pk=pk)
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student', 'student': student})


@login_required
@role_required(*ALL_ROLES)
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    attendance_pct = student.get_attendance_percentage()
    from apps.examinations.models import Result
    from apps.fees.models import FeePayment
    results = Result.objects.filter(student=student).order_by('-created_at')[:5]
    fee_status = FeePayment.objects.filter(student=student).order_by('-payment_date')[:5]
    return render(request, 'students/student_detail.html', {
        'student': student,
        'attendance_pct': attendance_pct,
        'results': results,
        'fee_status': fee_status,
    })


@login_required
@role_required(*ADMIN_ROLES)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.is_active = False
        student.save()
        messages.success(request, 'Student deactivated.')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


@login_required
@role_required(*ALL_ROLES)
def student_id_card(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/id_card.html', {'student': student})


@login_required
@role_required(*ADMIN_ROLES)
def student_promote(request):
    if request.method == 'POST':
        dept_id = request.POST.get('department')
        from_sem = int(request.POST.get('from_semester'))
        students = Student.objects.filter(department_id=dept_id, semester=from_sem, is_active=True)
        count = students.update(semester=from_sem + 1)
        messages.success(request, f'{count} students promoted to Semester {from_sem + 1}.')
        return redirect('student_list')
    departments = Department.objects.all()
    return render(request, 'students/promote.html', {'departments': departments})
