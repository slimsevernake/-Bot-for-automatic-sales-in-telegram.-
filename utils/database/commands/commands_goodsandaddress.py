from typing import List, Tuple

from django.db.models import Q, QuerySet
from loguru import logger

from asgiref.sync import sync_to_async
from ..commands import Goods, GoodsAndAddress


@sync_to_async
def select_goods_addresses(goods_pk: int, city: str) -> QuerySet[GoodsAndAddress]:
    try:
        addresses: QuerySet[GoodsAndAddress] = GoodsAndAddress.objects.filter(Q(goods__pk=goods_pk) &
                                                                              Q(address__city__city=city))
        return addresses
    except Exception as ex:
        logger.warning(f"GoodsAndAddress: {ex}")
