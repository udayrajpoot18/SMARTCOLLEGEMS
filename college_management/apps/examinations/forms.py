from django import forms
from .models import Exam, Result


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'exam_type', 'course', 'total_marks', 'passing_marks', 'exam_date', 'semester']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_type': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'exam', 'marks_obtained', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'exam': forms.Select(attrs={'class': 'form-select'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }
