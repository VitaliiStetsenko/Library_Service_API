from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer
from borrowings.models import Borrowings


class BorrowingsListRetrieveSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = Borrowings
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]

class BorrowingsCreateSerializer(serializers.ModelSerializer):
    actual_return_date = serializers.DateField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.filter(inventory__gt=0)
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Borrowings
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]