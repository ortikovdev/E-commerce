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
        fields = ['id', 'name', 'category', 'description', 'price', 'discount', 'images',
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