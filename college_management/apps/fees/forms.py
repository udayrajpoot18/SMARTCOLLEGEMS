from django import forms
from .models import FeeStructure, FeePayment


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'tuition_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'exam_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'library_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'other_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        exclude = ['transaction_id', 'created_at']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'fee_structure': forms.Select(attrs={'class': 'form-select'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }
