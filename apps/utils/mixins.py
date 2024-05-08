from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from apps.product.models import Trade


class CreateModelSetMixin:
    def create(self, request, *args, **kwargs):
        obj_id = super().create(request, *args, **kwargs).data.get('id')
        obj = get_object_or_404(Trade, id=obj_id)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)