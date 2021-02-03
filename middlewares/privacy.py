from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.database.commands.commands_user import select_user


class PrivacyMiddleware(BaseMiddleware):

    @staticmethod
    async def on_process_message(message: types.Message, data: dict):
        await get_user(msg=message, data=data)

    @staticmethod
    async def on_process_inline_query(query: types.InlineQuery, data: dict):
        await get_user(msg=query, data=data)


async def get_user(msg: types, data: dict):
    chat_id = int(msg.from_user.id)
    user = await select_user(chat_id=chat_id)
    data["user"] = user
