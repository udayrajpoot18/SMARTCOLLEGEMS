from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Teacher
from .forms import TeacherForm
from apps.core.models import Department
from apps.core.decorators import role_required, ADMIN_ROLES, ALL_ROLES


@login_required
@role_required(*ALL_ROLES)
def teacher_list(request):
    query = request.GET.get('q', '')
    dept_filter = request.GET.get('dept', '')
    teachers = Teacher.objects.select_related('department').filter(is_active=True)
    if query:
        teachers = teachers.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(employee_id__icontains=query) | Q(email__icontains=query)
        )
    if dept_filter:
        teachers = teachers.filter(department_id=dept_filter)
    paginator = Paginator(teachers, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    departments = Department.objects.all()
    return render(request, 'teachers/teacher_list.html', {
        'page_obj': page_obj, 'departments': departments,
        'query': query, 'dept_filter': dept_filter, 'total': teachers.count(),
    })


@login_required
@role_required(*ADMIN_ROLES)
def teacher_add(request):
    form = TeacherForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Teacher added successfully!')
        return redirect('teacher_list')
    return render(request, 'teachers/teacher_form.html', {'form': form, 'title': 'Add Teacher'})


@login_required
@role_required(*ADMIN_ROLES)
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(request.POST or None, request.FILES or None, instance=teacher)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Teacher updated successfully!')
        return redirect('teacher_detail', pk=pk)
    return render(request, 'teachers/teacher_form.html', {'form': form, 'title': 'Edit Teacher', 'teacher': teacher})


@login_required
@role_required(*ALL_ROLES)
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})


@login_required
@role_required(*ADMIN_ROLES)
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.is_active = False
        teacher.save()
        messages.success(request, 'Teacher deactivated.')
        return redirect('teacher_list')
    return render(request, 'teachers/teacher_confirm_delete.html', {'teacher': teacher})
