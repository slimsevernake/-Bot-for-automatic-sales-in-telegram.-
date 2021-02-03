import aiohttp

from data.config import CWD
from loader import bot


async def photo_link(path: str) -> str:
    with open(f"{CWD}/django_project/telegrambot/media/{path}", 'rb') as file:
        form = aiohttp.FormData()
        form.add_field(
            name="file",
            value=file
        )
        async with bot.session.post('https://telegra.ph/upload', data=form) as response:
            img_src = await response.json()

    link = 'http://telegra.ph/' + img_src[0]["src"]
    return link
