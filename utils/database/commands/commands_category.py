from loguru import logger

from asgiref.sync import sync_to_async

from ..commands import Category


@sync_to_async
def add_category(category: str, description: str = None) -> Category:
    try:
        new_category = Category.objects.create(category=category, description=description)
        logger.info(f"Category: {category}, successfully added.")
        return new_category
    except Exception as ex:
        logger.warning(f"Category: {ex}")


@sync_to_async
def select_category(category: str) -> Category:
    try:
        selected_category = Category.objects.get(category=category)
        logger.info(f"Category: {category}, successfully selected.")
        return selected_category
    except Exception as ex:
        logger.warning(f"Category: {ex}")
