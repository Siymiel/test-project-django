from django.urls import path
from .views import get_books, get_book, create_book

urlpatterns = [
    path("books/", get_books, name="get_books"),
    path("books/<int:pk>/", get_book, name="get_book"),
    path("books/create/", create_book, name="create_book")
]
