from aiogram import types

from django_project.telegrambot.usersmanage.models import User
# from handlers.inline.functions import sort_items_by_name
from handlers.inline.functions.sorts import sort_items_by_name, select_items_by_ilike
from loader import dp


@dp.inline_handler()
async def entry_in_query(query: types.InlineQuery, user: User):
    if user:
        ilike = query.query

        if ilike == "":
            list_items = await sort_items_by_name()
            await query.answer(**list_items.get_keys())
        else:
            if ':' in ilike:
                params = ilike.split(':')

                # Ошибка, параметров может быть только два - city или category
                if len(params) > 2:
                    return

                first = params[0].strip()
                second = params[1].strip()

                list_items = await select_items_by_ilike(first=first, second=second)
                await query.answer(**list_items.get_keys())
            else:
                param = ilike.strip()
                list_items = await select_items_by_ilike(first=param)
                await query.answer(**list_items.get_keys())
    else:
        await query.answer(
            results=[],
            switch_pm_text="Сперва зарегистрируйся!",
            switch_pm_parameter="registration",
        )
