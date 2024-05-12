from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.order.models import (
    Order,
    Promo,
    CartItem,
    OrderItem,
)
from apps.product.models import Product
from apps.product.serializers import ProductSerializer


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ['id', 'name', 'user', 'description', 'discount', 'min_price', 'expire_date', 'is_expired', 'members']

    def validate(self, attrs):
        if attrs.get('is_expired', True):
            raise ValidationError({'detail': 'Promo expired'})
        user = self.context['request'].user
        name = attrs.get('name')
        promo = Promo.objects.filter(name=name)
        if not promo.exists():
            raise ValidationError({'detail': 'Promo does not exist'})
        if user in promo.first().members.all():
            raise ValidationError({'detail': 'Promo already used'})
        if user in promo.last().members.all():
            return ValidationError({'detail': 'Promo already used'})
        return attrs

    def create(self, validated_data):
        name = validated_data['name']
        promo = Promo.objects.get(name=name)
        promo.members.add(self.context['request'].user)
        return promo


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'user', 'unit_price', 'quantity', 'amount', 'is_ordered', 'created_date',
                  'modified_date']
        read_only_fields = ['amount', 'user', 'is_ordered', 'created_date', 'modified_date']
        extra_kwargs = {
            'product': {'required': True},
            'quantity': {'required': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        quantity = validated_data.get('quantity', 1)
        product = Product.objects.get(id=validated_data['product'])
        validated_data['product_id'] = product.id
        validated_data['user_id'] = user.id
        validated_data['unit_price'] = product.price
        validated_data['amount'] = validated_data.get('quantity', 1) * validated_data['unit_price']
        validated_data['is_ordered'] = False
        return super().create(validated_data)


class CartItemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'user', 'unit_price', 'quantity', 'amount', 'is_ordered', 'created_date',
                  'modified_date']
        read_only_fields = ['amount', 'user', 'is_ordered', 'created_date', 'modified_date']
        extra_kwargs = {
            'product': {'required': True},
            'quantity': {'required': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_id'] = user.id
        validated_data['is_ordered'] = False
        return super().create(validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'user', 'unit_price', 'discount', 'quantity', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'promo', 'amount', 'modified_date', 'created_date']
        read_only_fields = ['created_date', 'modified_date']


class OrderPostSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'promo', 'amount', 'modified_date', 'created_date']
        read_only_fields = ['user', 'items', 'amount']

    def create(self, validated_data):
        user = self.context['request'].user
        items = validated_data.get('items', [])
        promo = Promo.objects.filter(name=validated_data['promo'])
        amount = 0
        cart_items = user.cart_items.all()
        order = super().create(validated_data)
        for cart_item in cart_items:
            amount += cart_item.get_amount
            oi = OrderItem.objects.create(
                product_id=cart_items.product.id,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price,
                discount=cart_item.product.discount,
                amount=cart_item.get_amount,
            )
            order.add(oi)
        if promo.exists():
            if promo.last().is_expired:
                raise ValidationError({'detail': 'Promo expired'})
            if user in promo.first().members.all():
                raise ValidationError({'detail': 'Promo already used'})
            if promo.min_price > amount:
                raise ValidationError({'detail': f'Must be less than or equal to {promo.min_price}'})
            amount = amount * (1 - promo.last().discount/100)
            promo.members.add(self.context['request'].user)
        order.amount = amount
        order.save()
        user.cart_items.all().delete()
        return order
