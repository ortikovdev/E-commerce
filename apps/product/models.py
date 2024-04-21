from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.account.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    views = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_quantity(self) -> int:
        incomes = self.trades.filter(quantity=1).count()
        outcomes = self.trades.filter(quantity=1).count()
        return incomes - outcomes

    def is_available(self) -> bool:
        return self.get_quantity() > 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d/')

    def __str__(self):
        return self.product.name


class Trade(models.Model):
    ACTION = (
        (1, _('Income')),
        (2, _('Outcome')),
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='trades')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.PositiveSmallIntegerField(choices=ACTION, default=1)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        incomes = Trade.objects.filter(product_id=self.product_id, action=1).count()
        outcomes = Trade.objects.filter(product_id=self.product_id, action=2).count()
        if incomes > outcomes:
            raise ValidationError(_("Outcomes cannot be greater than Incomes"))
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
