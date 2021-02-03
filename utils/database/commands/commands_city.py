from loguru import logger

from asgiref.sync import sync_to_async

from ..commands import City


@sync_to_async
def add_city(city: str) -> City:
    try:
        new_city = City.objects.create(city=city)
        logger.info(f"City: {city}, successfully added.")
        return new_city
    except Exception as ex:
        logger.warning(f"City: {ex}")


@sync_to_async
def select_city(city: str) -> City:
    try:
        selected_city = City.objects.get(city=city)
        logger.info(f"City: {city}, successfully selected.")
        return selected_city
    except Exception as ex:
        logger.warning(f"City: {ex}")
