from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    TagViewSet,
    ProductViewSet,
    ProductImageViewSet,
    TradeViewSet,
    WishlistViewSet,
    CommentViewSet,
)

app_name = 'product'

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('product_list', ProductViewSet)
router.register(r'(?P<pid>[0-9]+)/images', ProductImageViewSet)
router.register('wishlist', WishlistViewSet)
router.register('trades', TradeViewSet)
router.register(r'(?P<pid>[0-9]+)/comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
