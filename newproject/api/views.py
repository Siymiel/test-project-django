import logging
from .models import Book
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from .serializer import BookSerializer
from rest_framework import status # type: ignore
from rest_framework.exceptions import NotFound # type: ignore
from rest_framework.pagination import PageNumberPagination # type: ignore
from django.db import transaction

# Configure logging
logger = logging.getLogger(__name__)

# @api_view(['GET'])
# def get_books(request):
#     books = Book.objects.all()
#     serialized_data = BookSerializer(books, many=True).data
#     return Response(serialized_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_books(request):
    try:
        # Get query parameters from the request
        title = request.query_params.get('title', None)
        author = request.query_params.get('author', None)

        # Filter books based on query parameters (title or author)
        books = Book.objects.all()
        if title:
            books = books.filter(title__icontains=title)
        if author:
            books = books.filter(author__icontains=author)

        # Implement pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_books = paginator.paginate_queryset(books, request)

        # Serialize the paginated data
        serialized_data = BookSerializer(paginated_books, many=True).data

        return paginator.get_paginated_response(serialized_data)

    except Exception as e:
        logger.error(f"Error retrieving books: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
   
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

@api_view(['PUT'])
def update_book(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        logger.warning(f"Book with ID: {pk} not found")
        raise NotFound(detail="Book not found", code=404)

    serializer = BookSerializer(instance=book, data=request.data, partial=True)
    
    if serializer.is_valid():
        try:
            with transaction.atomic():
                book = serializer.save()
            
            logger.info(f"Book updated: {book.title} (ID: {book.id}) by user {request.user}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error updating book: {e}")
            return Response({"error": "Failed to update the book"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    logger.error(f"Error updating book: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# From the above:
# Transaction Management: The with transaction.atomic() block ensures that the update operation is atomic. If something goes wrong during the save process, the transaction will be rolled back.
# Partial Update: The partial=True argument in the serializer allows updating only the fields that are passed in the request data, leaving other fields unchanged.
# Enhanced Logging: The logging now includes the user who made the update request, which can be useful for auditing purposes.
# More Specific Error Responses: By catching exceptions in the transaction block, you can return a specific error message if something goes wrong during the save process.

@api_view(['DELETE'])
def delete_book(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        logger.warning(f"Book with ID: {pk} not found")
        raise NotFound(detail="Book not found", code=404)

    book.delete()
    logger.info(f"Book deleted: {book.title} (ID: {book.id}) by user {request.user}")
    return Response({"message": "Book deleted successfully"}, status=status.HTTP_200_OK)

