from typing import List, Tuple

from django.db.models import Q, QuerySet
from loguru import logger

from asgiref.sync import sync_to_async

from ..commands import Goods, Category, Address


@sync_to_async
def add_goods(name: str, description: str,
              category: Category, photo: str = None,
              cost: int = 0, quantity: int = 1) -> Goods:
    try:
        new_goods = Goods.objects.create(name=name, description=description,
                                         category=category, photo=photo,
                                         cost=cost, quantity=quantity)
        logger.info(f"Goods: {name} | {category} | {cost} | {quantity}, successfully added.")
        return new_goods
    except Exception as ex:
        logger.warning(f"Goods: {ex}")


@sync_to_async
def select_goods_by_pk(pk: int) -> Goods:
    try:
        selected_goods = Goods.objects.get(pk=pk)
        # logger.info(f"Goods: {goods.name} | {goods.category} | {goods.cost} | {goods.quantity}, successfully selected.")
        return selected_goods
    except Exception as ex:
        logger.warning(f"Goods: {ex}")


@sync_to_async
def select_goods_by_icontains(first: str, second: str = None) -> QuerySet[Goods]:
    if first and second:
        selected_goods = Goods.objects.filter(
            Q(address__city__city__icontains=first) & Q(category__category__icontains=second)
            | Q(address__city__city__icontains=second) & Q(category__category__icontains=first)
        ).distinct()
    else:
        selected_goods = Goods.objects.filter(
            Q(address__city__city__icontains=first) | Q(category__category__icontains=first)
        ).distinct()

    return selected_goods


@sync_to_async
def select_goods_quantity(pk: int) -> int:
    try:
        goods = Goods.objects.get(pk=pk)
        return goods.quantity
    except Exception as ex:
        logger.warning(f"Goods: {ex}")


@sync_to_async
def sort_goods_by_name() -> QuerySet[Goods]:
    try:
        sorted_goods = Goods.objects.order_by('name')
        return sorted_goods
    except Exception as ex:
        logger.warning(f"Goods: {ex}")


@sync_to_async
def count_and_return_goods_cities(pk: int) -> Tuple[int, QuerySet[Address]]:
    try:
        total_cities = Goods.objects.get(pk=pk).address.distinct('city').count()
        cities: QuerySet[Address] = Goods.objects.get(pk=pk).address.distinct('city')
        return total_cities, cities
    except Exception as ex:
        logger.warning(f"Goods: {ex}")


@sync_to_async
def update_new_photo_url(pk: int, new_photo_url: str) -> None:
    try:
        Goods.objects.filter(pk=pk).update(photo_url=new_photo_url)
    except Exception as ex:
        logger.warning(f"Goods: {ex}")


@sync_to_async
def update_goods_quantity(pk: int, new_quantity: int) -> None:
    try:
        Goods.objects.filter(pk=pk).update(quantity=new_quantity)
        logger.info(f"Goods: ({pk}) goods quantity successfully updated.")
    except Exception as ex:
        logger.warning(f"Goods: {ex}")
