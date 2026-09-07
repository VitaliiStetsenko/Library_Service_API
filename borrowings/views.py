from datetime import date

from django.conf import settings
from django.db import transaction

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

from payment.models import Payment
from payment.services import create_stripe_session


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
        queryset = (
            Borrowings.objects
            .select_related("book", "user")
            .prefetch_related("payments")
        )

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

    @transaction.atomic
    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)

        borrowing.book.inventory -= 1
        borrowing.book.save(update_fields=["inventory"])

        create_stripe_session(
            borrowing=borrowing,
            request=self.request,
            amount=borrowing.book.daily_fee,
            payment_type=Payment.PaymentType.PAYMENT,
        )

    @action(detail=True, methods=["post"], url_path="return")
    @transaction.atomic
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"detail": "Borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = date.today()
        borrowing.save(update_fields=["actual_return_date"])

        borrowing.book.inventory += 1
        borrowing.book.save(update_fields=["inventory"])

        if borrowing.actual_return_date > borrowing.expected_return_date:
            days_overdue = (
                    borrowing.actual_return_date
                    - borrowing.expected_return_date
            ).days

            fine_amount = (
                    days_overdue
                    * borrowing.book.daily_fee
                    * settings.FINE_MULTIPLIER
            )

            create_stripe_session(
                borrowing=borrowing,
                request=request,
                amount=fine_amount,
                payment_type=Payment.PaymentType.FINE,
            )

        return Response(
            {"detail": "Borrowing returned successfully."},
            status=status.HTTP_200_OK,
        )
