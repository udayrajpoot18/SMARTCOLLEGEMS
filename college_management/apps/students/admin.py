from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['enrollment_number', 'first_name', 'last_name', 'department', 'semester', 'is_active']
    list_filter = ['department', 'semester', 'is_active', 'gender']
    search_fields = ['enrollment_number', 'first_name', 'last_name', 'email']
