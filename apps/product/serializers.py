from rest_framework import serializers
from .models import (
    Category,
    Tag,
    Product,
    ProductImage,
    Trade,
    Like,
    Wishlist,
    Rank,
    Comment
)
from ..account.serializers import UserProfileSerializer


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []

    class Meta:
        model = Category
        fields = ['id', 'name', 'order', 'children']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'price', 'discount', 'views', 'images',
                  'tags', 'average_rank', 'get_quantity', 'get_like_count']
        read_only_fields = ['views', 'is_available']


class MiniProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'images',
                  'tags', 'average_rank', 'get_quantity', 'get_like_count']
        read_only_fields = ['views', 'is_avialable']


class ProductPostSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'price', 'discount', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        obj = super().create(validated_data)
        for image in images:
            ProductImage.objects.create(product=obj, images=open(image['images'], 'rb'))
        return obj


class TradeSerializer(serializers.ModelSerializer):
    product = MiniProductSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)
    action_name = serializers.CharField(read_only=True, source='get_action_display')

    class Meta:
        model = Trade
        fields = ['id', 'user', 'product', 'quantity', 'action', 'description', 'created_date']
        read_only_fields = ['user', 'product']


class TradePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = ['id', 'user', 'product', 'quantity', 'action', 'description', 'created_date']
        read_only_fields = ['user',]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_id'] = user.id
        return super().create(validated_data)
