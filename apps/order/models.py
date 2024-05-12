from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from rest_framework.exceptions import ValidationError

from apps.account.models import User
from apps.product.models import Product


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='cart_items')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_ordered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name}'

    @property
    def get_amount(self):
        return float(self.product.price) * ((self.product.discount or 1)/100)


class Promo(models.Model):
    name = models.CharField(max_length=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='promos')
    description = models.TextField(null=True, blank=True)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    min_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(250000)])
    members = models.ManyToManyField(User, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(CartItem)
    order_items = models.ManyToManyField(OrderItem)
    promo = models.CharField(max_length=8, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def get_amount(self):
        return sum(self.items.values_list('get_amount', flat=True))


def cart_item_pre_save(sender, instance, **kwargs):
    instance.unit_price = instance.product.price
    if instance.product.discount:
        amount = (instance.product.discount * instance.unit_price * instance.quantity) / 100
    else:
        amount = instance.unit_price * instance.quantity
    instance.amount = amount
    instance.save()


def order_pre_save(sender, instance, **kwargs):
    amount = sum(instance.cart_item.values_list('amount', flat=True))
    if instance.promo:
        if instance.promo not in Promo.objects.values_list('name', flat=True):
            raise ValidationError()


