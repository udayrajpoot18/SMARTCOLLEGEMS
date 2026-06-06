from django.urls import path
from . import views

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('add/', views.notice_add, name='notice_add'),
    path('<int:pk>/', views.notice_detail, name='notice_detail'),
    path('leave/', views.leave_list, name='leave_list'),
    path('leave/apply/', views.leave_apply, name='leave_apply'),
    path('leave/<int:pk>/review/', views.leave_review, name='leave_review'),
]
