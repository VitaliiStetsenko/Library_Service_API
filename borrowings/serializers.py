from rest_framework import serializers

from borrowings.models import Borrowings


class BorrowingsSerializer(serializers.ModelSerializer):
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
