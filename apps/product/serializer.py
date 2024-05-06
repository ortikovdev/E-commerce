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

