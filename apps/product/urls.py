from django.urls import path
from .views import CategoryViewSet

app_name = 'product'

urlpatterns = [
    path('searchby/category/<int:category_id>/', CategoryViewSet.as_view({'get': 'search_category'}), name='search-by-category'),
]
