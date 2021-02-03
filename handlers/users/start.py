from re import compile

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import get_start_link, decode_payload
from loguru import logger

from django_project.telegrambot.usersmanage.models import User, Goods
from filters import AdminFilter
from handlers.users.purchases import purchase_start_menu
from loader import dp
from utils.database.commands.commands_goods import select_goods_by_pk
from utils.database.commands.commands_user import add_user


# @dp.message_handler(CommandStart(), AdminFilter())
# async def bot_start(message: types.Message):
#     await message.answer(f"Привет admin, {message.from_user.full_name}!")


@dp.message_handler(CommandStart(deep_link=compile(r"^goods-\d+$")))
async def bot_start_buy_goods(message: types.Message, user: User):
    """Команда /start для покупки выбранного товара через inline mode"""
    if not user:
        await registration(message)

    args = (message.get_args()).replace('goods-', '')
    validation_on_exist_goods: Goods = await select_goods_by_pk(pk=int(args))

    if validation_on_exist_goods:
        await purchase_start_menu(message, goods=validation_on_exist_goods)
    else:
        logger.warning(f"{validation_on_exist_goods=}")


@dp.message_handler(CommandStart(deep_link="registration"))
async def bot_start_deeplink_from_inlinemode(message: types.Message, user: User):
    """Регистрация через inline mode"""

    if user:
        await already_registered(message)
    else:
        await registration(message)


@dp.message_handler(CommandStart(deep_link=compile(r"\d+"), encoded=True))
async def bot_start_deeplink(message: types.Message, user: User):
    """Переход по реф. ссылке"""

    if user:
        await already_registered(message)
    else:
        deep_link_args = message.get_args()
        decoded_link = int(decode_payload(deep_link_args))
        await registration(message, decoded_link)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, user: User):
    """Коданда /start без deep_link"""

    if user:
        await already_registered(message)
    else:
        await registration(message)


# Регистрация пользователя add_user() и приветствие already_registered()/success_registration() -----------------------
async def registration(message: types.Message, referral: int = None) -> None:
    user_id = message.chat.id
    username = message.from_user.username
    await success_registration(message, user_id=str(user_id))
    await add_user(chat_id=user_id, username=username, referral=referral)


# Функция успешной регистрации --------------------------------------------
async def success_registration(message: types.Message, user_id: str) -> None:
    deep_link = await get_start_link(payload=str(user_id), encode=True)
    await message.answer(f"Привет, {message.from_user.full_name}.\n"
                         f"Ты успешно зарегистрировался.\n"
                         f"Вот твоя реф. ссылка: {deep_link}\n\n"
                         f"Что бы узнать как пользоваться ботом введи комунду /help.",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Посмотреть товар", switch_inline_query_current_chat="")
                                 ]
                             ]
                         ))


# Функия для зарегистрированных пользователей ------------------------------
async def already_registered(message: types.Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}.\n",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Посмотреть товар", switch_inline_query_current_chat="")
                                 ]
                             ]
                         ))
