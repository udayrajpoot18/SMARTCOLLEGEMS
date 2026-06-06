from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Exam, Result
from .forms import ExamForm, ResultForm
from apps.students.models import Student
from apps.core.models import Course, Department
from apps.core.decorators import role_required, ADMIN_ROLES, TEACHER_ROLES, ALL_ROLES


@login_required
@role_required(*ALL_ROLES)
def exam_list(request):
    exams = Exam.objects.select_related('course').order_by('-exam_date')
    return render(request, 'examinations/exam_list.html', {'exams': exams})


@login_required
@role_required(*TEACHER_ROLES)
def exam_add(request):
    form = ExamForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Exam created successfully!')
        return redirect('exam_list')
    return render(request, 'examinations/exam_form.html', {'form': form, 'title': 'Create Exam'})


@login_required
@role_required(*TEACHER_ROLES)
def enter_marks(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    students = Student.objects.filter(
        department=exam.course.department, semester=exam.semester, is_active=True
    )
    if request.method == 'POST':
        count = 0
        for student in students:
            marks = request.POST.get(f'marks_{student.id}')
            if marks:
                Result.objects.update_or_create(
                    student=student, exam=exam,
                    defaults={'marks_obtained': float(marks)}
                )
                count += 1
        messages.success(request, f'Marks entered for {count} students.')
        return redirect('exam_list')
    existing = {r.student_id: r.marks_obtained for r in Result.objects.filter(exam=exam)}
    return render(request, 'examinations/enter_marks.html', {
        'exam': exam, 'students': students, 'existing': existing
    })


@login_required
@role_required(*ALL_ROLES)
def result_list(request):
    student_id = request.GET.get('student')
    dept_filter = request.GET.get('dept', '')
    results = Result.objects.select_related('student', 'exam', 'exam__course').order_by('-created_at')
    if student_id:
        results = results.filter(student_id=student_id)
    if dept_filter:
        results = results.filter(student__department_id=dept_filter)
    return render(request, 'examinations/result_list.html', {
        'results': results,
        'departments': Department.objects.all(),
        'dept_filter': dept_filter,
    })


@login_required
@role_required(*ALL_ROLES)
def student_result(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    results = Result.objects.filter(student=student).select_related('exam', 'exam__course')
    avg_gpa = results.aggregate(avg=Avg('grade_points'))['avg'] or 0
    return render(request, 'examinations/student_result.html', {
        'student': student, 'results': results, 'avg_gpa': round(avg_gpa, 2)
    })
