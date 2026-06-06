from django.urls import path
from . import views

urlpatterns = [
    path('', views.assignment_list, name='assignment_list'),
    path('add/', views.assignment_add, name='assignment_add'),
    path('<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),
    path('materials/', views.material_list, name='material_list'),
    path('materials/upload/', views.material_upload, name='material_upload'),
]
