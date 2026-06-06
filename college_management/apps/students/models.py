from django.db import models
from apps.core.models import User, Department, Course


class Student(models.Model):
    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    BLOOD_GROUP_CHOICES = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                           ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    enrollment_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1)
    address = models.TextField()
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)
    parent_email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    admission_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['enrollment_number']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_attendance_percentage(self):
        from apps.attendance.models import Attendance
        total = Attendance.objects.filter(student=self).count()
        present = Attendance.objects.filter(student=self, status='present').count()
        return round(present / total * 100, 1) if total > 0 else 0

    def __str__(self):
        return f"{self.enrollment_number} - {self.get_full_name()}"
