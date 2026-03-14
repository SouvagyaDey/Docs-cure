from rest_framework import serializers
from products.models import Product, ProductStore,ProductReview

class ProductReviewSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=ProductStore.objects.all())
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ProductReview
        fields = [
            "id", 
            "product", 
            "profile", 
            "rating", 
            "comment",
            "created_at", 
            "updated_at"
        ]


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    features = serializers.JSONField(required=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


    class Meta:
        model = Product
        fields = [
            'id',
            'features',
            'created_at',
            'updated_at'
        ]


class ProductStoreSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_data = ProductSerializer(write_only=True)
    product_reviews = ProductReviewSerializer(many=True, read_only=True)

    class Meta:
        model = ProductStore
        fields = [
            "id", 
            "product", 
            "product_data",
            "product_reviews",
            "name", 
            "price", 
            "description",
            "image_url",
            "category",
            "stock",
            "manufacturer", 
            "created_at", 
            "updated_at"
        ]

    def create(self, validated_data):
        product_data = validated_data.pop("product_data", None)
        if not product_data:
            raise serializers.ValidationError({"product_data": "This field is required."})


        features = product_data.get("features", None)

        if not features:
            raise serializers.ValidationError({"features": "This field is required."})

        product = Product.objects.using("products").create(features=features)

        return ProductStore.objects.create(product_id=product.id, **validated_data)


    def update(self, instance, validated_data):
        product_data = validated_data.pop("product_data", None)

        if product_data:
            product = Product.objects.using("products").get(id=instance.product_id)

            for attr, value in product_data.items():
                setattr(product, attr, value)

            product.save(using="products")

        return super().update(instance, validated_data)


    def to_representation(self, instance):

        rep = super().to_representation(instance)

        try:
            product = Product.objects.using("products").get(id=instance.product_id)
            rep["product"] = ProductSerializer(product).data

        except Product.DoesNotExist:
            rep["product"] = None
            
        return rep

