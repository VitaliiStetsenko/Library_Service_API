from django.urls import include, path
from rest_framework import routers

from payment.views import (
    PaymentCancelView,
    PaymentSuccessView,
    PaymentViewSet,
)

app_name = "payment"

router = routers.DefaultRouter()

router.register(
    "",
    PaymentViewSet,
    basename="payment",
)

urlpatterns = [
    path(
        "success/",
        PaymentSuccessView.as_view(),
        name="payment-success",
    ),
    path(
        "cancel/",
        PaymentCancelView.as_view(),
        name="payment-cancel",
    ),
    path("", include(router.urls)),
]
