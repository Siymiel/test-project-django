from django.urls import path # type: ignore
from .views import create_book, delete_book, get_book, get_books, update_book

urlpatterns = [
    path("books/", get_books, name="get_books"),
    path("books/<int:pk>/", get_book, name="get_book"),
    path("books/create/", create_book, name="create_book"),
    path("books/update/<int:pk>/", update_book, name="update_book"),
    path("books/delete/<int:pk>/", delete_book, name="delete_book")
]
