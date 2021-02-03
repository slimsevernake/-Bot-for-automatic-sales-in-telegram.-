from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .privacy import PrivacyMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(PrivacyMiddleware())
