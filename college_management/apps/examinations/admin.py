from django.contrib import admin
from .models import Exam, Result

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'course', 'exam_date', 'total_marks']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'marks_obtained', 'grade', 'grade_points']
    list_filter = ['grade', 'exam__exam_type']
