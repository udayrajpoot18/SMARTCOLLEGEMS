from django.contrib import admin
from .models import FeeStructure, FeePayment

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'semester', 'tuition_fee', 'academic_year']

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount_paid', 'payment_date', 'payment_method', 'status', 'transaction_id']
    list_filter = ['status', 'payment_method']
