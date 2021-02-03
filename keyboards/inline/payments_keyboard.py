from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

verification_cd = CallbackData("verification", "status")


# Клавиатура для monobank
async def mono_keyboard_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Оплатил", callback_data=verification_cd.new("paid"))
            ],
            [
                InlineKeyboardButton(text="Отмена", callback_data=verification_cd.new("cancel"))
            ]
        ]
    )

    return markup
