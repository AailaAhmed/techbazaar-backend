from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related("category")
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category__slug"]
    search_fields = ["title", "brand"]
    ordering_fields = ["price", "rating", "discount_percentage"]


from rest_framework import mixins
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        email = request.query_params.get("email", "").strip().lower()
        if email != order.email.lower():
            raise NotFound()
        return Response(self.get_serializer(order).data)
