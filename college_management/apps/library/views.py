from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Book, BookIssue
from .forms import BookForm, BookIssueForm
from apps.core.decorators import role_required, ADMIN_ROLES, TEACHER_ROLES, ALL_ROLES


@login_required
@role_required(*ALL_ROLES)
def book_list(request):
    query = request.GET.get('q', '')
    books = Book.objects.all()
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query))
    return render(request, 'library/book_list.html', {'books': books, 'query': query})


@login_required
@role_required(*ADMIN_ROLES)
def book_add(request):
    form = BookForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Book added to library!')
        return redirect('book_list')
    return render(request, 'library/book_form.html', {'form': form})


@login_required
@role_required(*TEACHER_ROLES)
def issue_book(request):
    form = BookIssueForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        issue = form.save(commit=False)
        book = issue.book
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()
            issue.save()
            messages.success(request, f'Book "{book.title}" issued successfully!')
        else:
            messages.error(request, 'No copies available.')
        return redirect('issued_books')
    return render(request, 'library/issue_form.html', {'form': form})


@login_required
@role_required(*TEACHER_ROLES)
def return_book(request, issue_id):
    issue = get_object_or_404(BookIssue, pk=issue_id)
    if request.method == 'POST':
        today = timezone.now().date()
        issue.return_date = today
        issue.status = 'returned'
        if today > issue.due_date:
            days_late = (today - issue.due_date).days
            issue.fine = days_late * 2
        issue.save()
        issue.book.available_copies += 1
        issue.book.save()
        messages.success(request, f'Book returned. Fine: ₹{issue.fine}')
        return redirect('issued_books')
    today = timezone.now().date()
    return render(request, 'library/return_confirm.html', {'issue': issue, 'today': today})


@login_required
@role_required(*ALL_ROLES)
def issued_books(request):
    issues = BookIssue.objects.select_related('book').filter(status='issued').order_by('due_date')
    today = timezone.now().date()
    for issue in issues:
        if issue.due_date < today:
            issue.status = 'overdue'
            issue.save()
    return render(request, 'library/issued_list.html', {'issues': issues, 'today': today})
