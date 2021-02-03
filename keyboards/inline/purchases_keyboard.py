import decimal

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from django.db.models import QuerySet

from django_project.telegrambot.usersmanage.models import Goods, Address, GoodsAndAddress
from utils.database.commands.commands_goods import count_and_return_goods_cities, select_goods_quantity
from utils.database.commands.commands_goodsandaddress import select_goods_addresses
from utils.database.commands.commands_payment import select_all_payments

purchase_cd = CallbackData("purchase", "level", "goods_pk", "city", "address", "quantity",
                           "payment", "amount_cost")
quantity_cd = CallbackData("quantity_btn", "operation", "quantity", "goods_pk", "city", "address")

order_cd = CallbackData("order", "goods_pk", "city", "address", "quantity", "payment", "amount_cost")


def make_purchase_cd(level, goods_pk, city="0", address="0", quantity="1",
                     payment="0", amount_cost="0") -> str:
    return purchase_cd.new(level=level, goods_pk=goods_pk, city=city, address=address, quantity=quantity,
                           payment=payment, amount_cost=amount_cost)


# Клавиатура для 0-го уровня меню
async def keyboard_start_menu(goods_pk: int, city: str = "0", step: int = 1) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0

    callback_data = make_purchase_cd(level=CURRENT_LEVEL + step, goods_pk=goods_pk, city=city)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Продолжить", callback_data=callback_data)
            ],
            [
                InlineKeyboardButton(text="Отмена", callback_data="cancel")
            ]
        ]
    )

    return markup


# Клавиатура для 1-го уровня меню
async def keyboard_cities_menu(goods_pk: int) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1

    count_city, cities = await count_and_return_goods_cities(pk=goods_pk)

    markup = InlineKeyboardMarkup(row_width=1)

    for city in cities:
        callback_data = make_purchase_cd(level=CURRENT_LEVEL + 1, goods_pk=goods_pk, city=city.city)
        button = InlineKeyboardButton(text=f"{city.city}", callback_data=callback_data)
        markup.insert(button)

    button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    markup.insert(button_cancel)

    return markup


# Клавиатура для 2-го уровня меню
async def keyboard_addresses_menu(goods_pk: int, city: str) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 2

    addresses: QuerySet[GoodsAndAddress] = await select_goods_addresses(goods_pk, city)

    markup = InlineKeyboardMarkup(row_width=1)

    for address in addresses:
        callback_data = make_purchase_cd(level=CURRENT_LEVEL + 1, goods_pk=goods_pk, city=city,
                                         address=address.address.address)
        button = InlineKeyboardButton(text=str(address.address), callback_data=callback_data)
        markup.insert(button)

    callback_data = make_purchase_cd(level=CURRENT_LEVEL - 1, goods_pk=goods_pk)
    await add_misc_buttons(markup, callback_data)

    return markup


# Клавиатура для 3-го уровня меню
async def keyboard_quantity_menu(goods_pk: int, city: str, address: str, quantity: int = 1) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 3

    callback_data = make_purchase_cd(level=CURRENT_LEVEL + 1, goods_pk=goods_pk,
                                     city=city, address=address, quantity=str(quantity))

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("➖",
                                     callback_data=quantity_cd.new(operation="➖", quantity=quantity,
                                                                   goods_pk=goods_pk, city=city, address=address)),
                InlineKeyboardButton(f"{quantity}", callback_data="quantity_button"),
                InlineKeyboardButton("➕",
                                     callback_data=quantity_cd.new(operation="➕", quantity=quantity,
                                                                   goods_pk=goods_pk, city=city, address=address))
            ],
            [
                InlineKeyboardButton(text="Продолжить", callback_data=callback_data)
            ]
        ],
        row_width=1
    )

    callback_data = make_purchase_cd(level=CURRENT_LEVEL - 1, goods_pk=goods_pk, city=city)
    await add_misc_buttons(markup, callback_data)

    return markup


# Клавиатура для 4-го уровня меню
async def keyboard_payment_menu(goods_pk: int, city: str, address: str, quantity: int) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 4

    markup = InlineKeyboardMarkup(row_width=1)

    payments = await select_all_payments()

    for payment in payments:
        callback_data = make_purchase_cd(level=CURRENT_LEVEL + 1, goods_pk=goods_pk,
                                         city=city, address=address, quantity=str(quantity), payment=payment.payment)
        button = InlineKeyboardButton(f"{payment.payment}", callback_data=callback_data)
        markup.insert(button)

    callback_data = make_purchase_cd(level=CURRENT_LEVEL - 1, goods_pk=goods_pk, city=city,
                                     address=address, quantity=str(quantity))
    await add_misc_buttons(markup, callback_data)

    return markup


# Клавиатура для 5-го уровня меню
async def keyboard_pre_order_menu(goods_pk: int, city: str, address: str, quantity: int,
                                  payment: str, amount_cost: decimal) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 5

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                # InlineKeyboardButton("Купить",
                #                      callback_data=purchase_cd.new(level=CURRENT_LEVEL + 1, goods_pk=goods_pk,
                #                                                    city=city, address=address,
                #                                                    quantity=quantity, payment=payment,
                #                                                    amount_cost=amount_cost))
                InlineKeyboardButton("Купить",
                                     callback_data=order_cd.new(goods_pk=goods_pk,
                                                                city=city, address=address,
                                                                quantity=quantity, payment=payment,
                                                                amount_cost=amount_cost))
            ]
        ],
        row_width=1
    )

    callback_data = make_purchase_cd(level=CURRENT_LEVEL - 1, goods_pk=goods_pk, city=city,
                                     address=address, quantity=str(quantity))
    await add_misc_buttons(markup, callback_data)

    return markup


# Добавление кнопок "Назад" и "Отмена" для каждой клавиатуре.
async def add_misc_buttons(markup: InlineKeyboardMarkup, callback_data: str) -> None:
    button_back = InlineKeyboardButton(text="Назад", callback_data=callback_data)
    button_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    markup.insert(button_back)
    markup.insert(button_cancel)
