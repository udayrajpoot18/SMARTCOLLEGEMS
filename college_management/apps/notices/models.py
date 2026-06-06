from django.db import models
from apps.core.models import User


class Notice(models.Model):
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')]
    TARGET_CHOICES = [('all', 'All'), ('students', 'Students'), ('teachers', 'Teachers')]
    title = models.CharField(max_length=200)
    content = models.TextField()
    target = models.CharField(max_length=20, choices=TARGET_CHOICES, default='all')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('sick', 'Sick Leave'), ('casual', 'Casual Leave'),
        ('emergency', 'Emergency'), ('other', 'Other'),
    ]
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=15, choices=LEAVE_TYPE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_leaves')
    review_remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def days(self):
        return (self.to_date - self.from_date).days + 1

    def __str__(self):
        return f"{self.applicant} - {self.leave_type} - {self.status}"
