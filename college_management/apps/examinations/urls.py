from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('add/', views.exam_add, name='exam_add'),
    path('<int:exam_id>/marks/', views.enter_marks, name='enter_marks'),
    path('results/', views.result_list, name='result_list'),
    path('results/student/<int:student_id>/', views.student_result, name='student_result'),
]
