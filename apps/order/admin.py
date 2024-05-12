from django.contrib import admin
from .models import CartItem, Order, Promo


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'get_amount', 'is_ordered', 'created_date')
    search_fields = ('product__title', 'user__username', 'user__full_name')
    date_hierarchy = 'created_date'
    list_filter = ('is_ordered',)
    readonly_fields = ('created_date',)


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'discount', 'min_price', 'expire_date', 'is_expired')
    list_filter = ('is_expired',)
    filter_horizontal = ('members',)
    date_hierarchy = 'created_date'
    readonly_fields = ('created_date',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_delivered', 'created_date')
    date_hierarchy = 'created_date'
    list_filter = ('is_delivered',)
    readonly_fields = ('get_amount', 'created_date', 'modified_date')
    search_fields = ('user__username', 'user__full_name')


