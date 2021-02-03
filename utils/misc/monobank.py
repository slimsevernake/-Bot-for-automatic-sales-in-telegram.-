import decimal
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

from monobank_api import PersonalAPI

from data.config import MONO_TOKEN, MONO_LINK

api = PersonalAPI(MONO_TOKEN)

time = datetime.now() - timedelta(minutes=6)
rate = (time, 0)


class NoPaymentFound(Exception):
    pass


class NotEnoughMoney(Exception):
    pass


@dataclass()
class Payment:
    amount_cost: decimal
    unique_comment: str = None

    # Информация для логирования
    goods_pk: int = None
    city: str = None
    address: str = None
    quantity: int = None
    payment: str = None

    def monobank_payment(self):
        self.__create_unique_comment_mono()
        return self.__invoice_mono

    # Создание уникального комментария к платежу MONOBANK
    def __create_unique_comment_mono(self):
        self.unique_comment = str(uuid.uuid4())
        return self.unique_comment

    # Проверка оплаты MONOBANK
    def check_payment_mono(self):
        date_from = datetime.now() - timedelta(days=1)
        statements = api.get_statements(account=0, date_to=datetime.now(), date_from=date_from)

        for statement in statements:
            amount_statement = statement.get("amount")
            comment_statement = statement.get("comment")

            if comment_statement:
                if str(self.unique_comment) in comment_statement:
                    if float(amount_statement) >= float(self.amount_cost):
                        return True
                    else:
                        raise NotEnoughMoney

        else:
            raise NoPaymentFound

    # Ссылка ддля оплаты MONOBANK
    @property
    def __invoice_mono(self):
        mono_link = MONO_LINK
        return mono_link


class MonoPayment(Payment):
    pass


# @dataclass()
# class MonoPayment:
#     amount_cost: decimal
#     unique_comment: str = None
#
#     # Информация для логирования
#     goods_pk: int = None
#     city: str = None
#     address: str = None
#     quantity: int = None
#     payment: str = None
#
#     # Создание уникального комментария к платежу
#     def create_unique_comment(self):
#         self.unique_comment = str(uuid.uuid4())
#         return self.unique_comment
#
#     # Проверка оплаты
#     def check_payment(self):
#         date_from = datetime.now() - timedelta(days=1)
#         statements = api.get_statements(account=0, date_to=datetime.now(), date_from=date_from)
#
#         for statement in statements:
#             amount_statement = statement.get("amount")
#             comment_statement = statement.get("comment")
#
#             if comment_statement:
#                 if str(self.unique_comment) in comment_statement:
#                     if float(amount_statement) >= float(self.amount_cost):
#                         return True
#                     else:
#                         raise NotEnoughMoney
#
#         else:
#             raise NoPaymentFound
#
#     @property
#     def invoice(self):
#         mono_link = MONO_LINK
#         return mono_link
