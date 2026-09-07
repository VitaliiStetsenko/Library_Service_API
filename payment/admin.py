from django.contrib import admin

from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "borrowing",
        "type",
        "status",
        "money_to_pay",
        "created_at",
    )

    list_filter = (
        "status",
        "type",
    )

    search_fields = (
        "user__email",
        "session_id",
    )