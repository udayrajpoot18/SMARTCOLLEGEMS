from django.db import models
from apps.students.models import Student
from apps.teachers.models import Teacher
from apps.core.models import Course


class Assignment(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('closed', 'Closed')]
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignments')
    deadline = models.DateTimeField()
    total_marks = models.IntegerField(default=10)
    file = models.FileField(upload_to='assignments/teacher/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course}"


class Submission(models.Model):
    STATUS_CHOICES = [('submitted', 'Submitted'), ('graded', 'Graded'), ('late', 'Late')]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='assignments/student/', blank=True, null=True)
    text_response = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks_obtained = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f"{self.student} - {self.assignment}"


class StudyMaterial(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('notes', 'Notes'), ('pdf', 'PDF'), ('ppt', 'Presentation'),
        ('video', 'Video Link'), ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='study_materials')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='study_materials')
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPE_CHOICES)
    file = models.FileField(upload_to='study_materials/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course}"
