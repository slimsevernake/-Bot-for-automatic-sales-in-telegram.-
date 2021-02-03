from asgiref.sync import sync_to_async
from loguru import logger

from ..commands import User


# Добавление нового пользователя ------------------------------------------
@sync_to_async
def add_user(chat_id: int, username: str, referral: int = None) -> User:
    try:
        new_user = User.objects.create(chat_id=chat_id, username=username, referral=referral)
        logger.info(f"User: {username}({chat_id}), successfully added.")
        return new_user
    except Exception as ex:
        logger.warning(f"User: {ex}")


# Поиск пользователя по chat_id --------------------------------------------
@sync_to_async
def select_user(chat_id: int) -> User:
    try:
        user = User.objects.get(chat_id=chat_id)
        logger.info(f"User: {user.username}({chat_id}), successfully selected.")
    except Exception as ex:
        user = None
        logger.warning(f"User: {ex}")

    return user


@sync_to_async
def update_user_ordered(chat_id: int) -> None:
    try:
        User.objects.filter(chat_id=chat_id).update(ordered=True)
        logger.info(f"User: ({chat_id}), successfully updated ordered status.")
    except Exception as ex:
        logger.warning(f"User: {ex}")


@sync_to_async
def update_user_successful_purchases(chat_id: int, new_quantity) -> None:
    try:
        User.objects.filter(chat_id=chat_id).update(successful_purchases=new_quantity)
        logger.info(f"User: ({chat_id}), successfully updated successful purchases.")
    except Exception as ex:
        logger.warning(f"User: {ex}")
