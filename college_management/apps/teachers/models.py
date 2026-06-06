from django.db import models
from apps.core.models import User, Department, Course


class Teacher(models.Model):
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('hod', 'Head of Department'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    specialization = models.CharField(max_length=200, blank=True)
    qualification = models.CharField(max_length=100)
    experience_years = models.IntegerField(default=0)
    joining_date = models.DateField()
    photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True)
    subjects = models.ManyToManyField(Course, blank=True, related_name='teachers')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.employee_id} - {self.get_full_name()}"
