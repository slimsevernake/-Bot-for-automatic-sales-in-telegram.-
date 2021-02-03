from typing import List

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from django_project.telegrambot.usersmanage.models import Goods
from loader import bot
from utils import photo_link
from utils.database.commands.commands_goods import update_new_photo_url


async def generate_list_InlineQueryResultArticle(sorted_items: List[Goods]):
    items_list = list()

    for sorted_item in sorted_items:
        if sorted_item.quantity >= 1:
            try:
                cities = ", ".join([str(address.city) for address in sorted_item.address.distinct('city')])

                bot_username = (await bot.me).username

                if sorted_item.photo_url:
                    photo_url = sorted_item.photo_url
                elif sorted_item.photo:
                    photo_url = await photo_link(str(sorted_item.photo))
                    await update_new_photo_url(pk=sorted_item.pk, new_photo_url=photo_url)
                else:
                    photo_url = ""

                items_list.append(
                    types.InlineQueryResultArticle(
                        id=str(sorted_item.pk),
                        title=sorted_item.name,
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"<b>{sorted_item.name}</b>\n\n"
                                         f"<b>Категория: </b>{sorted_item.category}\n"
                                         f"<b>Доступные города: </b>{cities}\n"
                                         f"<b>Описание: </b>{sorted_item.description}\n"
                                         f"<i>{sorted_item.cost} грн</i>"
                        ),
                        description=f"({sorted_item.category}) {sorted_item.cost} грн.\n"
                                    f"({cities})\n\n"
                                    f"{sorted_item.description}",
                        thumb_url=photo_url,
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text='Купить',
                                                         url=f"https://t.me/{bot_username}?start=goods-{sorted_item.pk}")
                                ]
                            ]
                        )
                    )
                )
            except Exception as ex:
                logger.warning(ex)

    return items_list
