from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import path

from .models import User, Category, City, Payment, Goods, SuccessfulPurchase, FailedPurchase, Address, GoodsAndAddress


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'username', 'referral', 'ordered',
                    'successful_purchases', 'created_at', 'updated_at')
    list_display_links = ('id', 'chat_id', 'username')
    list_filter = ('ordered', 'created_at', 'updated_at')
    search_fields = ('id', 'chat_id', 'username')

    def has_add_permission(self, request):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'description', 'created_at', 'updated_at')
    list_display_links = ('id', 'category')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('id', 'category')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'created_at')
    list_display_links = ('id', 'city')
    list_filter = ('city', 'created_at')
    search_fields = ('id', 'city')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'view_city_link', 'created_at', 'updated_at')
    list_display_links = ('id', 'address')
    list_filter = ('address', 'city__city', 'created_at', 'updated_at')
    search_fields = ('id', 'address', 'city__city')

    def view_city_link(self, obj):
        city_name = obj.city.city
        url = reverse('admin:usersmanage_city_change', args=[obj.city.pk])
        return format_html('<a href="{}">{}</a>', url, city_name)

    view_city_link.short_description = 'Город'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'created_at')
    list_display_links = ('id', 'payment')
    list_filter = ('payment', 'created_at')
    search_fields = ('id', 'payment')


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'view_category_link', 'cost', 'quantity', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'category__category', 'created_at', 'updated_at')
    search_fields = ('id', 'name', 'category__category')

    def view_category_link(self, obj):
        category_name = obj.category.category
        # url = f"http://127.0.0.1:8000/admin/usersmanage/category/{obj.category.id}/change/"
        url = reverse('admin:usersmanage_category_change', args=[obj.category.pk])
        return format_html('<a href="{}">{}</a>', url, category_name)

    view_category_link.short_description = 'Категория'


@admin.register(GoodsAndAddress)
class GoodsAndAddress(admin.ModelAdmin):
    list_display = ('id', 'view_goods_link', 'view_address_link', 'created_at', 'updated_at')
    list_display_links = ('id',)
    list_filter = ('goods', 'address', 'created_at', 'updated_at',)
    search_fields = ('id', 'goods__name', 'address__address')

    def view_goods_link(self, obj):
        goods = obj.goods
        url = reverse('admin:usersmanage_goods_change', args=[obj.goods.pk])
        return format_html('<a href="{}">{}</a>', url, goods)

    view_goods_link.short_description = 'Название товара'

    def view_address_link(self, obj):
        address = obj.address
        url = reverse('admin:usersmanage_address_change', args=[obj.address.pk])
        return format_html('<a href="{}">{}</a>', url, address)

    view_address_link.short_description = 'Адрес'


@admin.register(FailedPurchase)
class FailedPurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'view_user_id_link', 'view_goods_link', 'quantity', 'amount_cost',
                    'view_payment_link', 'created_at', 'updated_at')
    list_display_links = ('id',)
    list_filter = ('updated_at', 'goods', 'payment__payment',)
    search_fields = ('id', 'quantity', 'chat_id__chat_id', 'goods__name', 'payment__payment',)

    def view_user_id_link(self, obj):
        chat_id = obj.chat_id
        url = reverse('admin:usersmanage_user_history', args=[obj.chat_id.pk])
        return format_html('<a href="{}">{}</a>', url, chat_id)

    view_user_id_link.short_description = 'ID Пользователя'

    def view_goods_link(self, obj):
        goods = obj.goods
        url = reverse('admin:usersmanage_goods_history', args=[obj.goods.pk])
        return format_html('<a href="{}">{}</a>', url, goods)

    view_goods_link.short_description = 'Название товара'

    def view_payment_link(self, obj):
        payment = obj.payment
        url = reverse('admin:usersmanage_payment_history', args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>', url, payment)

    view_payment_link.short_description = 'Способ оплаты'


@admin.register(SuccessfulPurchase)
class SuccessfulPurchaseAdmin(FailedPurchaseAdmin):
    pass
