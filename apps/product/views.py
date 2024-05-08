from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .models import (
    Category,
    Tag, Product, ProductImage,
)
from .serializer import (
    CategorySerializer,
    TagSerializer,
    ProductSerializer,
    ProductPostSerializer,
    ProductImageSerializer,
)
from .permissions import (
    IsAdminOrReadOnly,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ['name']

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True)

    def get_object(self):
        queryset = self.queryset
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg),
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ['name']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    serializer_post_class = ProductPostSerializer

    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['name']
    filterset_fields = ['category', 'tags']
    ordering_fields = ['views', 'id', 'sold_count']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return super().get_serializer_class()
        return self.serializer_post_class

    def create(self, request, *args, **kwargs):
        obj_id = super().create(request, *args, **kwargs).get('id')
        obj = get_object_or_404(Product, id=obj_id)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        pid = self.kwargs.get('pid')
        if pid:
            return ProductImage.objects.filter(product_id=pid)
        return ProductImage.objects.none()

    def get_serializer_context(self):
        pid = self.kwargs.get('pid')
        ctx = super().get_serializer_context()
        ctx['pid'] = pid
        return ctx