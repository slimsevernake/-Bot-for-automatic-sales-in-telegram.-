from loguru import logger

from asgiref.sync import sync_to_async
from django.db.models import QuerySet

from ..commands import Payment


@sync_to_async
def add_payment(payment: str) -> Payment:
    try:
        new_payment = Payment.objects.create(payment=payment)
        logger.info(f"Payment: {payment}, successfully added.")
        return new_payment
    except Exception as ex:
        logger.info(f"Payment: {ex}")


@sync_to_async
def select_all_payments() -> QuerySet[Payment]:
    try:
        selected_payments: QuerySet[Payment] = Payment.objects.all()
        return selected_payments
    except Exception as ex:
        logger.info(f"Payment: {ex}")


@sync_to_async
def select_payment(payment: str) -> Payment:
    try:
        selected_payment = Payment.objects.get(payment=payment)
        logger.info(f"Payment: {payment}, successfully selected.")
        return selected_payment
    except Exception as ex:
        logger.info(f"Payment: {ex}")
