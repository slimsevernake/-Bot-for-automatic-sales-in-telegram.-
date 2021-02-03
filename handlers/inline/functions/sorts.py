from dataclasses import dataclass
from typing import List

from aiogram import types

from django_project.telegrambot.usersmanage.models import Goods
from handlers.inline.functions.generate_list_goods import generate_list_InlineQueryResultArticle
from utils.database.commands.commands_goods import sort_goods_by_name, select_goods_by_icontains


@dataclass
class ShowItems:
    results: List[types.InlineQueryResultArticle]

    def get_keys(self):
        return self.__dict__


async def sort_items_by_name() -> ShowItems:
    sorted_items: List[Goods] = await sort_goods_by_name()
    generated_list_InlineQueryResultArticle = await generate_list_InlineQueryResultArticle(sorted_items)

    result = ShowItems(results=generated_list_InlineQueryResultArticle)
    return result


async def select_items_by_ilike(first: str, second: str = None) -> ShowItems:
    selected_items: List[Goods] = await select_goods_by_icontains(first=first, second=second)
    generated_list_InlineQueryResultArticle = await generate_list_InlineQueryResultArticle(selected_items)

    result = ShowItems(results=generated_list_InlineQueryResultArticle)
    return result
