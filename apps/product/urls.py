from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    TagViewSet,
    ProductViewSet,
    ProductImageViewSet,
    TradeViewSet,
    WishlistViewSet,
    LikeSerializer,
    RankViewSet,
    CommentViewSet,
)

app_name = 'product'

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register(r'(?P<pid>[0-9]+)/images', ProductImageViewSet)
router.register('(trades)', TradeViewSet)
router.register('wishlist', WishlistViewSet)
# router.register('likes', LikeViewSet)
router.register(r'(?P<pid>[0-9]+)/ranks', RankViewSet)
router.register(r'(?P<pid>[0-9]+)/comments', CommentViewSet)
router.register('product_list', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
