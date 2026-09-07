from decimal import Decimal

import stripe


def create_stripe_session(
    borrowing,
    request,
    amount,
    payment_type,
):
    success_url = request.build_absolute_uri(
        "/api/payments/success/"
        "?session_id={CHECKOUT_SESSION_ID}"
    )

    cancel_url = request.build_absolute_uri(
        "/api/payments/cancel/"
    )

    checkout_session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": borrowing.book.title,
                    },
                    "unit_amount": int(
                        Decimal(amount) * Decimal("100")
                    ),
                },
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
    )

    from payment.models import Payment

    return Payment.objects.create(
        status=Payment.PaymentStatus.PENDING,
        type=payment_type,
        money_to_pay=amount,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
        borrowing=borrowing,
        user=borrowing.user,
    )
