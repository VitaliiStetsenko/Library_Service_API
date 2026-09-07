from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "money_to_pay",
            "session_url",
            "session_id",
            "borrowing",
            "user",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "type",
            "session_url",
            "session_id",
            "user",
            "created_at",
        ]
