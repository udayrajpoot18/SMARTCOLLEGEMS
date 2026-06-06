from django.db import models
from apps.students.models import Student
from apps.core.models import Course


class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('internal', 'Internal'), ('mid_term', 'Mid Term'),
        ('semester', 'Semester End'), ('practical', 'Practical'),
    ]
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    total_marks = models.IntegerField(default=100)
    passing_marks = models.IntegerField(default=40)
    exam_date = models.DateField()
    semester = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course}"


class Result(models.Model):
    GRADE_CHOICES = [
        ('O', 'Outstanding (O)'), ('A+', 'Excellent (A+)'), ('A', 'Very Good (A)'),
        ('B+', 'Good (B+)'), ('B', 'Above Average (B)'), ('C', 'Average (C)'),
        ('F', 'Fail (F)'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.FloatField()
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, blank=True)
    grade_points = models.FloatField(default=0)
    remarks = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'exam']

    def save(self, *args, **kwargs):
        pct = (self.marks_obtained / self.exam.total_marks) * 100
        if pct >= 90:
            self.grade, self.grade_points = 'O', 10.0
        elif pct >= 80:
            self.grade, self.grade_points = 'A+', 9.0
        elif pct >= 70:
            self.grade, self.grade_points = 'A', 8.0
        elif pct >= 60:
            self.grade, self.grade_points = 'B+', 7.0
        elif pct >= 50:
            self.grade, self.grade_points = 'B', 6.0
        elif pct >= 40:
            self.grade, self.grade_points = 'C', 5.0
        else:
            self.grade, self.grade_points = 'F', 0.0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.grade}"
