from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.main.models import Order, Tag
from apps.main.serializers import OrderSerializer, TagSerializer


class OrdersViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [AllowAny]


class TagsViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
