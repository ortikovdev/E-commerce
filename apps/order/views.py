from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.order.models import Order, OrderItem, CartItem, Promo
from apps.order.serializer import PromoSerializer, CartItemSerializer, OrderSerializer, OrderPostSerializer
from apps.utils.mixins import CreateViewSetMixin


class CheckPromo(generics.GenericAPIView):
    serializer_class = PromoSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)
    queryset = CartItem.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class OrderViewSet(CreateViewSetMixin, viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    model = Order
    serializer_post_class = OrderPostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return self.serializer_class