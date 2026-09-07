import stripe
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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
            "borrowing__book",
            "user",
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)


class PaymentSuccessView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        session_id = request.query_params.get("session_id")

        if not session_id:
            return Response(
                {"detail": "session_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe.StripeError:
            return Response(
                {"detail": "Unable to retrieve Stripe session."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = Payment.objects.filter(
            session_id=session_id
        ).first()

        if not payment:
            return Response(
                {"detail": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if session.payment_status == "paid":
            payment.status = Payment.PaymentStatus.PAID
            payment.save(update_fields=["status"])

            return Response(
                {
                    "detail": "Payment was successful.",
                    "payment_id": payment.id,
                }
            )

        return Response(
            {
                "detail": "Payment has not been completed.",
                "payment_id": payment.id,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class PaymentCancelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                "detail": (
                    "Payment was cancelled. "
                    "You can complete it later."
                )
            },
            status=status.HTTP_200_OK,
        )
