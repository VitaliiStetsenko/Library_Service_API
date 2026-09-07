from rest_framework import viewsets

from books.views import DefaultPagination
from borrowings.models import Borrowings
from borrowings.serializers import BorrowingsSerializer


class BorrowingsViewSet(viewsets.ModelViewSet):
    queryset = Borrowings.objects.all()
    serializer_class = BorrowingsSerializer
    pagination_class = DefaultPagination
