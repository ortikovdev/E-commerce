from django.contrib import admin
from .models import CartItem, Order


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'unit_price', 'quantity', 'is_ordered', 'created_date')
    list_filter = ('product__name', 'is_ordered')
    search_fields = ('product__title', 'user')
    date_hierarchy = 'created_date'
    readonly_fields = ('created_date', 'modified_date')
    ordering = ('-created_date',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_delivered', 'created_date')
    search_fields = ('user__username', 'user__full_name')