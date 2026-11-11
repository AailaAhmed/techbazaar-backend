from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "title", "description", "brand", "price",
            "discount_percentage", "rating", "stock",
            "thumbnail", "category",
        ]


from django.db import transaction
from .models import Order, OrderItem


class OrderItemInputSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="product.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["title", "quantity", "unit_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemInputSerializer(many=True, write_only=True)
    lines = OrderItemSerializer(source="items", many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "full_name", "email", "phone", "address", "postal_code",
            "country", "payment_method", "status", "total", "created_at",
            "items", "lines",
        ]
        read_only_fields = ["id", "status", "total", "created_at"]

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("items")
        order = Order.objects.create(total=0, **validated_data)
        total = 0
        for line in items:
            product = (
                Product.objects.select_for_update()
                .filter(id=line["product"], is_active=True)
                .first()
            )
            if product is None:
                raise serializers.ValidationError(f"Product {line['product']} not found.")
            if product.stock < line["quantity"]:
                raise serializers.ValidationError(f"Not enough stock for {product.title}.")
            product.stock -= line["quantity"]
            product.save(update_fields=["stock"])
            OrderItem.objects.create(
                order=order, product=product,
                quantity=line["quantity"], unit_price=product.price,
            )
            total += product.price * line["quantity"]
        order.total = total
        order.save(update_fields=["total"])
        return order
