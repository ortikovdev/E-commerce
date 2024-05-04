from rest_framework import viewsets
from rest_framework.response import Response
from .models import Category
from .serializer import CategorySerializer


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        category = self.queryset.get(pk=pk)
        serializer = self.serializer_class(category)
        return Response(serializer.data)

    def search_category(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        parents = category.get_parents()
        queryset = Category.objects.filter(id__in=parents)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
