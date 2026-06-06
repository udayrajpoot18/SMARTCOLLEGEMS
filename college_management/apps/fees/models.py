from django.db import models
from apps.students.models import Student
from apps.core.models import Department


class FeeStructure(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='fee_structures')
    semester = models.IntegerField()
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    academic_year = models.CharField(max_length=10, default='2024-25')

    @property
    def total_fee(self):
        return self.tuition_fee + self.exam_fee + self.library_fee + self.other_fee

    def __str__(self):
        return f"{self.name} - Sem {self.semester}"


class FeePayment(models.Model):
    STATUS_CHOICES = [('paid', 'Paid'), ('pending', 'Pending'), ('partial', 'Partial')]
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Online'), ('cash', 'Cash'), ('dd', 'DD'), ('cheque', 'Cheque')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='online')
    transaction_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='paid')
    remarks = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.amount_paid} - {self.status}"
