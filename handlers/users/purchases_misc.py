from aiogram.types import CallbackQuery

from django_project.telegrambot.usersmanage.models import Goods
from keyboards.inline.purchases_keyboard import quantity_cd, keyboard_quantity_menu
from loader import dp

from utils.database.commands.commands_goods import select_goods_quantity


# Отменить покупку -----------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text_contains="cancel")
async def cancel_button(call: CallbackQuery):
    await call.message.delete()


@dp.callback_query_handler(quantity_cd.filter())
async def quantity_button_enlarge(call: CallbackQuery, callback_data: dict):
    goods_pk = callback_data.get("goods_pk")
    city = callback_data.get("city")
    address = callback_data.get("address")
    operation = callback_data.get("operation")
    quantity = int(callback_data.get("quantity"))

    goods_exist = await select_goods_quantity(goods_pk)

    if operation == "➕" and quantity < goods_exist:
        quantity += 1
    elif operation == "➖" and quantity != 1:
        quantity -= 1
    elif operation == "➕" and quantity == goods_exist:
        await call.answer("На складе больше товара нету!!!", cache_time=15, show_alert=True)
    elif operation == "➖" and quantity == 1:
        await call.answer("Количество товара не может равняться нулю!!!", cache_time=15, show_alert=True)

    markup = await keyboard_quantity_menu(goods_pk=goods_pk, city=city, address=address, quantity=quantity)
    await call.message.edit_reply_markup(markup)


# Template для текста товара и нового шага.
async def template_goods_text(goods: Goods, text_next_step: str = None) -> str:
    template = f"<b>{goods.name}</b>\n\n" \
               f"Всего на складе: {goods.quantity} шт.\n" \
               f"Цена за 1 шт: {goods.cost} грн.\n\n" \
               f"{goods.description}\n\n"

    if text_next_step:
        template += f"🠗🠗🠗<b>{text_next_step}</b>🠗🠗🠗"

    return template
