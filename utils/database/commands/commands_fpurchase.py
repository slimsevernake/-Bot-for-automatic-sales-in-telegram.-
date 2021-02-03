import decimal

from loguru import logger

from asgiref.sync import sync_to_async

from ..commands import FailedPurchase, User, Payment


@sync_to_async
def add_failed_purchase(chat_id: User, goods_id: int,
                        quantity: int, amount_cost: decimal, payment: Payment) -> FailedPurchase:
    try:
        new_failed_purchase = FailedPurchase.objects.create(chat_id=chat_id, goods_id=goods_id, quantity=quantity,
                                                            amount_cost=amount_cost, payment=payment)
        logger.info(f"FailedPurchase: {new_failed_purchase.pk}(id), successfully added")
        return new_failed_purchase
    except Exception as ex:
        logger.warning(f"FailedPurchase: {ex}")
