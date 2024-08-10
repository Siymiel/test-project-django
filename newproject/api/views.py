from .models import Book
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from .serializer import BookSerializer
from rest_framework import status # type: ignore


@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serialized_data = BookSerializer(books, many=True).data
    return Response(serialized_data)
