from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
)

app_name = 'product'

router = DefaultRouter()
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
