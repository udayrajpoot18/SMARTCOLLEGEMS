from django.contrib import admin
from .models import Book, BookIssue

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'category', 'total_copies', 'available_copies']
    search_fields = ['title', 'author', 'isbn']

@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'student_name', 'student_id', 'issue_date', 'due_date', 'status', 'fine']
    list_filter = ['status']
