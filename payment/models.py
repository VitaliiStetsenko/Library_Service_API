from django.conf import settings
from django.db import models


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    type = models.CharField(
        max_length=20,
        choices=PaymentType.choices,
        default=PaymentType.PAYMENT,
    )
    money_to_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    session_url = models.URLField(
        blank=True,
        null=True,
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    borrowing = models.ForeignKey(
        "borrowings.Borrowings",
        on_delete=models.CASCADE,
        related_name="payments",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.type} - {self.money_to_pay}"
