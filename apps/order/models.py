from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from apps.account.models import User
from apps.product.models import Product


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='cart_items')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_ordered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name}'

    @property
    def get_amount(self):
        return self.quantity * self.unit_price


class Promo(models.Model):
    name = models.CharField(max_length=8, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    min_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(250000)])
    expire_date = models.DateField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    members = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    promo = models.CharField(max_length=8, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def get_amount(self):
        return sum(self.items.values_list('get_amount', flat=True))