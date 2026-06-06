from django.urls import path
from . import views

urlpatterns = [
    path('', views.fee_dashboard, name='fee_dashboard'),
    path('structure/', views.fee_structure_list, name='fee_structure_list'),
    path('structure/add/', views.fee_structure_add, name='fee_structure_add'),
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/new/', views.make_payment, name='make_payment'),
    path('payments/<int:payment_id>/receipt/', views.fee_receipt, name='fee_receipt'),
    path('student/<int:student_id>/', views.student_fee_status, name='student_fee_status'),
]
