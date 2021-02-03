from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, bot


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    username = (await bot.get_me()).username
    await message.answer(f"<b>Helper</b>\n\n"
                         f"Для того что бы начать пользоваться ботом, достаточно ввести юзернейм бота в любом чате.\n"
                         f"Далее следует указать город и категорию товара, разделяя их двоеточием ':' (можно комбинировать).\n\n"
                         f"⬇⬇⬇ ПРИМЕРЫ ВВОДА ⬇⬇⬇\n\n"
                         f"@{username} Город\n"
                         f"@{username} Категория\n"
                         f"@{username} Город:Категория\n"
                         f"@{username} Категория:Город\n\n"
                         f"⬇⬇⬇<b>Так же посмотреть товар можно по кнопке</b>⬇⬇⬇",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Посмотреть товар", switch_inline_query_current_chat="")
                                 ]
                             ]
                         ))
