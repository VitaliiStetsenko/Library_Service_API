from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from books.models import Book
from books.permisions import AdminAllOrReadOnly
from books.serializers import BookSerializer


class DefaultPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


class BooksViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [AdminAllOrReadOnly]
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Book.objects.all()

        title = self.request.query_params.get("title", None)
        author = self.request.query_params.get("author", None)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            queryset = queryset.filter(author__icontains=author)

        return queryset
