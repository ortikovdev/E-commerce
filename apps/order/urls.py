from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.order.models import Order
from apps.order.views import (
    OrderViewSet,
    CheckPromo,
    CartItemViewSet,
)

app_name = 'order'

router = DefaultRouter()
router.register('cartitem', CartItemViewSet, basename='cartitem')
router.register('', OrderViewSet, basename='order')

urlpatterns = [
    path('', CheckPromo.as_view(), name='check_promo'),
    path('', include(router.urls)),
]