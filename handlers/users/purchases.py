from typing import Union, Tuple

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from django.db.models import QuerySet

from django_project.telegrambot.usersmanage.models import Goods
from handlers.users.purchases_misc import template_goods_text
from keyboards.inline import keyboard_start_menu, keyboard_cities_menu, keyboard_quantity_menu, keyboard_addresses_menu
from keyboards.inline.purchases_keyboard import purchase_cd, keyboard_payment_menu, keyboard_pre_order_menu
from loader import dp
from utils.database.commands.commands_goods import count_and_return_goods_cities, select_goods_by_pk


# CURRENT_LEVER = 0
async def purchase_start_menu(message: Message, goods: Goods):
    count_city, cities = await count_and_return_goods_cities(pk=goods.pk)

    if count_city == 1:
        city = cities[0].city.city
        markup = await keyboard_start_menu(goods.pk, city, step=2)
    else:
        markup = await keyboard_start_menu(goods.pk)

    template = await template_goods_text(goods)
    if goods.photo_url == '':
        await message.answer(text=template, reply_markup=markup)
    else:
        await message.answer_photo(photo=goods.photo_url, caption=template, reply_markup=markup)


# CURRENT_LEVER = 1. Если город у товара только один - данный шаг пропуск.
async def purchase_city_menu(call: CallbackQuery, goods_pk: int, **kwargs):
    goods: Goods = await select_goods_by_pk(goods_pk)

    markup = await keyboard_cities_menu(goods.pk)
    text_next_step = "Выберете город"

    template = await template_goods_text(goods, text_next_step)

    if goods.photo_url == '':
        await call.message.edit_text(text=template, reply_markup=markup)
    else:
        await call.message.edit_caption(caption=template, reply_markup=markup)


# CURRENT_LEVER = 2
async def purchase_address_menu(call: CallbackQuery, goods_pk: int, city: str, **kwargs):
    goods: Goods = await select_goods_by_pk(goods_pk)

    markup = await keyboard_addresses_menu(goods_pk, city)
    text_next_step = "Выберете адрес"

    template = await template_goods_text(goods, text_next_step)

    if goods.photo_url == '':
        await call.message.edit_text(text=template, reply_markup=markup)
    else:
        await call.message.edit_caption(caption=template, reply_markup=markup)


# CURRENT_LEVER = 3
async def purchase_quantity_menu(call: CallbackQuery, goods_pk: int, city: str,
                                 address: str, quantity: int, **kwargs):
    goods: Goods = await select_goods_by_pk(goods_pk)

    markup = await keyboard_quantity_menu(goods_pk, city, address, quantity)
    text_next_step = "Выберете количество товара"

    template = await template_goods_text(goods, text_next_step)

    if goods.photo_url == '':
        await call.message.edit_text(text=template, reply_markup=markup)
    else:
        await call.message.edit_caption(caption=template, reply_markup=markup)


# CURRENT_LEVER = 4
async def purchase_payment_menu(call: CallbackQuery, goods_pk: int, city: str, address: str, quantity: int, **kwargs):
    goods: Goods = await select_goods_by_pk(goods_pk)

    markup = await keyboard_payment_menu(goods_pk, city, address, quantity)
    text_next_step = "Выберете способ оплаты"

    template = await template_goods_text(goods, text_next_step)

    if goods.photo_url == '':
        await call.message.edit_text(text=template, reply_markup=markup)
    else:
        await call.message.edit_caption(caption=template, reply_markup=markup)


# CURRENT_LEVER = 5
async def purchase_pre_order_menu(call: CallbackQuery, goods_pk: int, city: str,
                                  address: str, quantity: int, payment: str, **kwargs):
    goods: Goods = await select_goods_by_pk(goods_pk)

    amount_cost = goods.cost * quantity

    template = f"<b>{goods.name}</b>\n\n" \
               f"Цена за 1 шт: {goods.cost} грн\n" \
               f"Количество товара в вашей корзине: <b>{quantity}</b>\n" \
               f"<b>Итого к оплате: {amount_cost} грн</b>\n\n" \
               f"Вы заказали товар на указанный адрес: <b>{city}. {address}</b>\n\n" \
               f"Способ оплаты: <b>{payment}</b>"

    markup = await keyboard_pre_order_menu(goods_pk, city, address, quantity, payment, amount_cost)

    if goods.photo_url == '':
        await call.message.edit_text(text=template, reply_markup=markup)
    else:
        await call.message.edit_caption(caption=template, reply_markup=markup)


# Навигация по меню ----------------------------------------------------------------------------------------------------
@dp.callback_query_handler(purchase_cd.filter())
async def navigation_keyboards(call: CallbackQuery, callback_data: dict):
    await call.answer()
    current_level = callback_data.get("level")
    goods_pk = callback_data.get("goods_pk")
    city = callback_data.get("city")
    address = callback_data.get("address")
    quantity = int(callback_data.get("quantity"))
    payment = callback_data.get("payment")
    amount_cost = callback_data.get("amount_cost")

    levels = {
        "1": purchase_city_menu,
        "2": purchase_address_menu,
        "3": purchase_quantity_menu,
        "4": purchase_payment_menu,
        "5": purchase_pre_order_menu,
    }
    current_level_function = levels[current_level]

    await current_level_function(
        call,
        goods_pk=goods_pk,
        city=city,
        address=address,
        quantity=quantity,
        payment=payment,
        amount_cost=amount_cost
    )
