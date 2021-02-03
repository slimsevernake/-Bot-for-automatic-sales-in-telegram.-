import decimal

from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink, hcode

from django_project.telegrambot.usersmanage.models import Goods
from keyboards.inline import mono_keyboard_markup
from keyboards.inline.payments_keyboard import verification_cd
from keyboards.inline.purchases_keyboard import order_cd
from loader import dp
from aiogram.types import Message, CallbackQuery

from utils.database.commands.commands_fpurchase import add_failed_purchase
from utils.database.commands.commands_goods import select_goods_by_pk
from utils.database.commands.commands_payment import select_payment
from utils.database.commands.commands_spurchase import add_successful_purchase
from utils.database.commands.commands_user import select_user, update_user_ordered, update_user_successful_purchases
from utils.misc.monobank import MonoPayment, NoPaymentFound, NotEnoughMoney, Payment


@dp.callback_query_handler(order_cd.filter())
async def purchase_order_menu(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()

    goods_pk = callback_data.get("goods_pk")
    city = callback_data.get("city")
    address = callback_data.get("address")
    quantity = int(callback_data.get("quantity"))
    payment = callback_data.get("payment")
    amount_cost = callback_data.get("amount_cost")

    goods: Goods = await select_goods_by_pk(goods_pk)

    template = ""
    markup = await mono_keyboard_markup()

    if payment == "monobank":
        mono_payment = MonoPayment(amount_cost=amount_cost, goods_pk=goods_pk, city=city,
                                   address=address, quantity=quantity, payment=payment)
        invoice_mono = mono_payment.monobank_payment()

        template = f"<b>{goods.name}</b>\n\n" \
                   f"Цена за 1 шт: {goods.cost} грн\n" \
                   f"Количество товара в вашей корзине: <b>{quantity}</b>\n" \
                   f"<b>Итого к оплате: {amount_cost} грн</b>\n\n" \
                   f"Вы заказали товар на указанный адрес: <b>{city}. {address}</b>\n\n" \
                   f"Способ оплаты: <b>{payment}</b>\n\n" \
                   f"Оплатите {amount_cost} грн по ссылке 👉🏻👉🏻👉🏻{hlink(title='оплатить', url=invoice_mono)}👈🏻👈🏻👈🏻\n\n" \
                   f"И обязательно укажите ID платежа в комментарий:\n" \
                   f"{hcode(mono_payment.unique_comment)}\n\n" \
                   f"Затем нажмите кнопку \"Оплатил\"."

        await state.set_state("verification")
        await state.update_data(payment=mono_payment)

    if goods.photo_url == '':
        await call.message.edit_text(text=template, reply_markup=markup)
    else:
        await call.message.edit_caption(caption=template, reply_markup=markup)


# Проверка на оплату
@dp.callback_query_handler(verification_cd.filter(status="paid"), state="verification")
async def purchase_paid(call: CallbackQuery, state: FSMContext):
    await call.answer()
    payment: Payment = (await state.get_data()).get("payment")

    try:
        if payment.payment == "monobank":
            payment.check_payment_mono()
    except NoPaymentFound:
        await call.message.answer("Транзакция не найдена.")
        return
    except NotEnoughMoney:
        await call.message.answer("Оплаченная сума меньше необходимой.")
        return

    else:
        await info_to_db_about_purchase(call, state, payment, status=True)

        goods: Goods = await select_goods_by_pk(payment.goods_pk)
        await call.message.answer(f"Вы успешно оплатили товар: <b>{goods.name}</b> - {payment.quantity} шт.\n\n"
                                  f"Адрес: {payment.address}\n"
                                  f"Сума заказа: {payment.amount_cost} грн.\n"
                                  f"Способ оплаты: {payment.payment}")


# Отмена покупки
@dp.callback_query_handler(verification_cd.filter(status="cancel"), state="verification")
async def purchase_cancel(call: CallbackQuery, state: FSMContext):
    await call.answer("Вы отменили покупку!", show_alert=True)
    payment: Payment = (await state.get_data()).get("payment")

    await info_to_db_about_purchase(call, state, payment, status=False)


# Информация о заказе 'Оплачен товар или покупка была отменена'
async def info_to_db_about_purchase(call: CallbackQuery, state: FSMContext, payment: Payment, status: bool):
    await call.message.delete()
    await state.finish()

    chat_id = call.from_user.id
    user = await select_user(chat_id=chat_id)
    selected_payment = await select_payment(payment=payment.payment)

    if status:
        await add_successful_purchase(chat_id=user, goods_id=payment.goods_pk, quantity=payment.quantity,
                                      amount_cost=payment.amount_cost, payment=selected_payment)

        # Изминение кол-во успешн. покупок, товара на складе и т.д. и т.п.
        user.successful_purchases = user.successful_purchases + 1
        # await update_user_successful_purchases(chat_id, new_quantity)

        goods: Goods = await select_goods_by_pk(payment.goods_pk)
        goods.quantity = goods.quantity - payment.quantity
        goods.save()

        if not user.ordered:
            user.ordered = True
            # await update_user_ordered(chat_id=chat_id)
        user.save()
    else:
        await add_failed_purchase(chat_id=user, goods_id=payment.goods_pk, quantity=payment.quantity,
                                  amount_cost=payment.amount_cost, payment=selected_payment)
