from django.db import models


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('textbook', 'Textbook'), ('reference', 'Reference'),
        ('novel', 'Novel'), ('magazine', 'Magazine'), ('journal', 'Journal'),
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    publisher = models.CharField(max_length=100, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    rack_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class BookIssue(models.Model):
    STATUS_CHOICES = [('issued', 'Issued'), ('returned', 'Returned'), ('overdue', 'Overdue')]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')
    fine = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.book.title} - {self.student_name}"
