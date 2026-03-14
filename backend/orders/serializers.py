from rest_framework import serializers
from orders.models import Order, OrderItem
from products.models import ProductStore
from products.serializers import ProductStoreSerializer
from django.db import transaction


class OrderItemReadSerializer(serializers.ModelSerializer):
    """Read-only serializer that includes product details."""
    id = serializers.UUIDField(read_only=True)
    product = ProductStoreSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "subtotal"]


class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    product = ProductStoreSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product",
            "product_id",
            "quantity",
            "subtotal"
        ]
        extra_kwargs = {
            "order": {"read_only": True},
        }


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "profile",
            "status",
            "shipping_address",
            "updated_at",
            "total_amount",
            "order_items",
            "created_at"
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("order_items", None)
        if not items_data:
            raise serializers.ValidationError({"items": "Order must contain at least one item."})

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in items_data:
                product_uuid = item.pop("product_id")
                quantity = item.get("quantity", 1)

                try:
                    store_product = ProductStore.objects.select_for_update().get(id=product_uuid)
                except ProductStore.DoesNotExist:
                    raise serializers.ValidationError({"product": f"Product {product_uuid} does not exist."})

                if store_product.stock < quantity:
                    raise serializers.ValidationError({
                        "stock": f"Not enough stock for {store_product.name}. "
                                 f"Available: {store_product.stock}, Requested: {quantity}"
                    })

                store_product.stock -= quantity
                store_product.save(update_fields=["stock"])

                OrderItem.objects.create(
                    order=order,
                    product=store_product,
                    quantity=quantity,
                )

            order.update_total()

        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['order_items'] = OrderItemReadSerializer(instance.order_items.all(), many=True).data
        return rep