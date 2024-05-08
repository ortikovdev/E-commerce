from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    TagViewSet,
    ProductViewSet,
    ProductImageViewSet,
)

app_name = 'product'

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('product_list', ProductViewSet)
router.register(r'(?P<pid>[0-9]+)/images', ProductImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
