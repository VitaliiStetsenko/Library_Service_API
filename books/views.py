from rest_framework import viewsets

from books.models import Book
from books.permisions import AdminAllOrReadOnly
from books.serializers import BookSerializer


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AdminAllOrReadOnly]
