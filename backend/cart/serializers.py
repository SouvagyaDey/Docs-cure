from rest_framework import serializers
from .models import Cart, CartItem
from products.models import ProductStore
from products.serializers import ProductStoreSerializer

class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cart = serializers.PrimaryKeyRelatedField(read_only=True)
    product = ProductStoreSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductStore.objects.all(), write_only=True, source="product"
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "product",
            "product_id",
            "quantity",
            'created_at',
            'updated_at'
        ]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    cart_items = CartItemSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


    class Meta:
        model = Cart
        fields = [
            "id", 
            "profile", 
            "cart_items", 
            "created_at"
        ]