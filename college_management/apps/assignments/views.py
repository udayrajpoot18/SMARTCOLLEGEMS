from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assignment, Submission, StudyMaterial
from .forms import AssignmentForm, SubmissionForm, StudyMaterialForm
from apps.core.models import Course
from apps.core.decorators import role_required, TEACHER_ROLES, ALL_ROLES


@login_required
@role_required(*ALL_ROLES)
def assignment_list(request):
    assignments = Assignment.objects.select_related('course', 'teacher').order_by('-created_at')
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments})


@login_required
@role_required(*TEACHER_ROLES)
def assignment_add(request):
    form = AssignmentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Assignment created!')
        return redirect('assignment_list')
    return render(request, 'assignments/assignment_form.html', {'form': form, 'title': 'Create Assignment'})


@login_required
@role_required(*ALL_ROLES)
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    submissions = assignment.submissions.select_related('student').all()
    return render(request, 'assignments/assignment_detail.html', {
        'assignment': assignment, 'submissions': submissions
    })


@login_required
@role_required('student', 'teacher', 'super_admin', 'principal')
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    form = SubmissionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        sub = form.save(commit=False)
        sub.assignment = assignment
        sub.save()
        messages.success(request, 'Assignment submitted successfully!')
        return redirect('assignment_list')
    return render(request, 'assignments/submit_form.html', {'form': form, 'assignment': assignment})


@login_required
@role_required(*ALL_ROLES)
def material_list(request):
    materials = StudyMaterial.objects.select_related('course', 'teacher').order_by('-created_at')
    return render(request, 'assignments/material_list.html', {'materials': materials})


@login_required
@role_required(*TEACHER_ROLES)
def material_upload(request):
    form = StudyMaterialForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Material uploaded successfully!')
        return redirect('material_list')
    return render(request, 'assignments/material_form.html', {'form': form})
