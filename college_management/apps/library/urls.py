from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_add, name='book_add'),
    path('issue/', views.issue_book, name='issue_book'),
    path('issued/', views.issued_books, name='issued_books'),
    path('return/<int:issue_id>/', views.return_book, name='return_book'),
]
