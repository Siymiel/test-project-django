import logging
from .models import Book
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from .serializer import BookSerializer
from rest_framework import status # type: ignore
from rest_framework.exceptions import NotFound # type: ignore

# Configure logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serialized_data = BookSerializer(books, many=True).data
    return Response(serialized_data)

@api_view(['GET'])
def get_book(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        raise NotFound(detail="Book not found", code=404)
    
    serialized_data = BookSerializer(book, many=False).data
    return Response(serialized_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        book = serializer.save()
        
        logger.info(f"Book created: {book.title} (ID: {book.id})")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    logger.error(f"Error creating book: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
