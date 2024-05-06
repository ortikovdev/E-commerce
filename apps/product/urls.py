from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
)

app_name = 'product'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    # path('searchby/category/<int:category_id>/', CategoryViewSet.as_view({'get': 'search_category'}), name='search-by-category'),
]
