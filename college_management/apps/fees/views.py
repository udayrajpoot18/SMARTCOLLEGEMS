from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from .models import FeeStructure, FeePayment
from .forms import FeeStructureForm, FeePaymentForm
from apps.students.models import Student
from apps.core.decorators import role_required, ADMIN_ROLES, ALL_ROLES
import uuid


@login_required
@role_required(*ALL_ROLES)
def fee_dashboard(request):
    total_collected = FeePayment.objects.filter(status='paid').aggregate(total=Sum('amount_paid'))['total'] or 0
    pending_count = FeePayment.objects.filter(status='pending').count()
    recent_payments = FeePayment.objects.select_related('student').order_by('-payment_date')[:10]
    return render(request, 'fees/dashboard.html', {
        'total_collected': total_collected,
        'pending_count': pending_count,
        'recent_payments': recent_payments,
    })


@login_required
@role_required(*ALL_ROLES)
def fee_structure_list(request):
    structures = FeeStructure.objects.select_related('department').all()
    return render(request, 'fees/structure_list.html', {'structures': structures})


@login_required
@role_required(*ADMIN_ROLES)
def fee_structure_add(request):
    form = FeeStructureForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Fee structure created!')
        return redirect('fee_structure_list')
    return render(request, 'fees/structure_form.html', {'form': form})


@login_required
@role_required(*ALL_ROLES)
def payment_list(request):
    payments = FeePayment.objects.select_related('student').order_by('-payment_date')
    student_filter = request.GET.get('student', '')
    status_filter = request.GET.get('status', '')
    if student_filter:
        payments = payments.filter(
            Q(student__first_name__icontains=student_filter) |
            Q(student__enrollment_number__icontains=student_filter)
        )
    if status_filter:
        payments = payments.filter(status=status_filter)
    return render(request, 'fees/payment_list.html', {
        'payments': payments, 'status_filter': status_filter
    })


@login_required
@role_required(*ADMIN_ROLES)
def make_payment(request):
    form = FeePaymentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        payment = form.save(commit=False)
        payment.transaction_id = f"TXN{uuid.uuid4().hex[:10].upper()}"
        payment.save()
        messages.success(request, f'Payment recorded! Transaction ID: {payment.transaction_id}')
        return redirect('payment_list')
    return render(request, 'fees/payment_form.html', {'form': form})


@login_required
@role_required(*ALL_ROLES)
def fee_receipt(request, payment_id):
    payment = get_object_or_404(FeePayment, pk=payment_id)
    return render(request, 'fees/receipt.html', {'payment': payment})


@login_required
@role_required(*ALL_ROLES)
def student_fee_status(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    payments = FeePayment.objects.filter(student=student).order_by('-payment_date')
    total_paid = payments.filter(status='paid').aggregate(total=Sum('amount_paid'))['total'] or 0
    return render(request, 'fees/student_fee.html', {
        'student': student, 'payments': payments, 'total_paid': total_paid
    })
