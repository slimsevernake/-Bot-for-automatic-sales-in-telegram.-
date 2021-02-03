import os

import django

from utils.misc.logger import setup_logger
from utils.notify_admins import on_startup_notify

from utils.set_bot_commands import set_default_commands


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "django_project.telegrambot.telegrambot.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


async def on_startup(dp):
    import filters
    import middlewares

    filters.setup(dp)
    middlewares.setup(dp)

    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])

    setup_django()

    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
