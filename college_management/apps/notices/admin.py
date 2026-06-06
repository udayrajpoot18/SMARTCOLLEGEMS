from django.contrib import admin
from .models import Notice, LeaveRequest

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'target', 'priority', 'created_by', 'is_active', 'created_at']
    list_filter = ['target', 'priority', 'is_active']

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'leave_type', 'from_date', 'to_date', 'status']
    list_filter = ['status', 'leave_type']
