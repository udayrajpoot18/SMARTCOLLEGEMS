from django.contrib import admin
from .models import Assignment, Submission, StudyMaterial

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'teacher', 'deadline', 'status']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'submitted_at', 'status', 'marks_obtained']

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'teacher', 'material_type', 'created_at']
