from rest_framework import serializers

from apps.order.models import (
    Order,
    Promo,
)


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ['id', 'name', 'user', 'description', 'discount', 'min_price', 'expire_date', 'members']