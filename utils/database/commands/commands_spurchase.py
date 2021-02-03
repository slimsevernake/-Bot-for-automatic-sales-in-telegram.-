import decimal

from loguru import logger

from asgiref.sync import sync_to_async

from ..commands import SuccessfulPurchase, User, Payment


@sync_to_async
def add_successful_purchase(chat_id: User, goods_id: int,
                            quantity: int, amount_cost: decimal, payment: Payment) -> SuccessfulPurchase:
    try:
        new_successful_purchase = SuccessfulPurchase.objects.create(chat_id=chat_id, goods_id=goods_id,
                                                                    quantity=quantity, amount_cost=amount_cost,
                                                                    payment=payment)
        logger.info(f"SuccessfulPurchase: {new_successful_purchase.pk}(id), successfully added")
        return new_successful_purchase
    except Exception as ex:
        logger.warning(f"SuccessfulPurchase: {ex}")
