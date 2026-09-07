from rest_framework import mixins, viewsets

from books.views import DefaultPagination
from payment.models import Payment
from payment.permissions import IsAuthenticatedAndOwnerOrAdmin
from payment.serializers import PaymentSerializer


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedAndOwnerOrAdmin]
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Payment.objects.select_related(
            "borrowing",
            "book",
            "user",
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)
