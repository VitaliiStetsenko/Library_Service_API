from datetime import date

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from books.views import DefaultPagination
from borrowings.models import Borrowings
from borrowings.permissions import AdminAllAuthenticatedReadPostDelete
from borrowings.serializers import (
    BorrowingsListRetrieveSerializer,
    BorrowingsCreateSerializer,
)


class BorrowingsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowings.objects.select_related("book", "user")
    pagination_class = DefaultPagination
    permission_classes = [AdminAllAuthenticatedReadPostDelete]

    def get_queryset(self):
        queryset = Borrowings.objects.select_related("book", "user")
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        is_active = self.request.query_params.get("is_active")

        if is_active == "true":
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif is_active == "false":
            queryset = queryset.filter(actual_return_date__isnull=False)

        user_id = self.request.query_params.get("user_id")

        if self.request.user.is_staff and user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingsCreateSerializer
        return BorrowingsListRetrieveSerializer

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)

        borrowing.book.inventory -= 1
        borrowing.book.save()

    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        borrowing = Borrowings.objects.select_related("book", "user").get(pk=pk)

        if request.user != borrowing.user and not request.user.is_staff:
            return Response(
                {"detail": "You are not the borrower of this book"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if borrowing.actual_return_date:
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = date.today()
        borrowing.save()

        borrowing.book.inventory += 1
        borrowing.book.save()

        return Response(
            self.get_serializer(borrowing).data,
            status=status.HTTP_200_OK,
        )
