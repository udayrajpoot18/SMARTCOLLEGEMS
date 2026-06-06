from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_dashboard, name='attendance_dashboard'),
    path('take/', views.take_attendance, name='take_attendance'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('student/<int:student_id>/', views.student_attendance_detail, name='student_attendance_detail'),
    path('get-students/', views.get_students_for_course, name='get_students_for_course'),
]
