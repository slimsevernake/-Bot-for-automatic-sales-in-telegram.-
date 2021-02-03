from django.db import models


class TimedBaseModels(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')


class User(TimedBaseModels):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    chat_id = models.BigIntegerField(unique=True, db_index=True, verbose_name='ID Пользователя')
    username = models.CharField(max_length=50, verbose_name='Username')
    referral = models.BigIntegerField(null=True, blank=True, verbose_name='Реферер')
    ordered = models.BooleanField(default=False, verbose_name='Делал покупки')
    successful_purchases = models.IntegerField(default=0, verbose_name='Кол-во успешных покупок')

    def __str__(self):
        return str(self.chat_id)


class Category(TimedBaseModels):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    category = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Категория')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.category


class City(TimedBaseModels):
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    city = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Город')

    def __str__(self):
        return self.city


class Address(TimedBaseModels):
    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    city = models.ForeignKey(City, on_delete=models.CASCADE, db_index=True, verbose_name='Город')
    address = models.CharField(max_length=50, db_index=True, verbose_name='Адрес')

    def __str__(self):
        return f"{self.city}: {self.address}"


class Payment(TimedBaseModels):
    class Meta:
        verbose_name = "Платежная система"
        verbose_name_plural = "Платежные системы"

    payment = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Платежная система')

    def __str__(self):
        return self.payment


class Goods(TimedBaseModels):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    name = models.CharField(max_length=50, verbose_name='Название товара')
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey('Category', db_index=True, on_delete=models.CASCADE, verbose_name='Категория')
    address = models.ManyToManyField('Address', db_index=True, through='GoodsAndAddress')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    photo_url = models.TextField(null=True, blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=8, null=True, default=0, verbose_name='Цена')
    quantity = models.IntegerField(null=True, default=1, verbose_name='На складе')

    def __str__(self):
        return self.name


class GoodsAndAddress(TimedBaseModels):
    class Meta:
        verbose_name = "Товары-адрес"
        verbose_name_plural = "Товары-адреса"

    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='Название товара')
    address = models.ForeignKey('Address', on_delete=models.CASCADE, verbose_name='Адрес')


class SuccessfulPurchase(TimedBaseModels):
    class Meta:
        verbose_name = "Успешная покупка"
        verbose_name_plural = "Успешные покупки"

    chat_id = models.ForeignKey('User', db_index=True, on_delete=models.CASCADE, verbose_name='ID Пользователя')
    goods = models.ForeignKey('Goods', db_index=True, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    amount_cost = models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Сума")
    payment = models.ForeignKey('Payment', db_index=True, on_delete=models.CASCADE, verbose_name='Способ оплаты')

    def __str__(self):
        return f"SuccessfulPurchase - {self.chat_id} | {self.goods} | {self.quantity} | {self.payment}"


class FailedPurchase(TimedBaseModels):
    class Meta:
        verbose_name = "Неудачная покупка"
        verbose_name_plural = "Неудачные покупки"

    chat_id = models.ForeignKey('User', db_index=True, on_delete=models.CASCADE, verbose_name='ID Пользователя')
    goods = models.ForeignKey('Goods', db_index=True, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    amount_cost = models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Сума")
    payment = models.ForeignKey('Payment', db_index=True, on_delete=models.CASCADE, verbose_name='Способ оплаты')

    def __str__(self):
        return f"FailedPurchase - {self.chat_id} | {self.goods} | {self.quantity} | {self.payment}"
