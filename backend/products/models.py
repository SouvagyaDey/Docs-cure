from django.db import models
from django.db.models import Q
from authy.models import Profile
import uuid

class ProductCategory(models.TextChoices):
    MEDICINE = "medicine", "Medicine"
    EQUIPMENT = "equipment", "Equipment"
    WELLNESS = "wellness", "Wellness"
    FITNESS = "fitness", "Fitness"



class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    features = models.JSONField(default=dict, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

        
    def delete(self, using=None, keep_parents=False):
        ProductStore.objects.filter(product_id=self.id).delete()
        super().delete(using="products", keep_parents=keep_parents)
        
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        managed = False
    

class ProductStore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.UUIDField()
    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=100,
        choices=ProductCategory.choices,
        default=ProductCategory.MEDICINE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Product image URL")
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ProductStore"
        verbose_name_plural = "ProductStores"

        constraints = [
            models.CheckConstraint(
                name='price_non_negative',
                check=Q(price__gte=0),
                violation_error_message='Price must be a non-negative number.'
            )
        ]
    



class ProductReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProductStore, on_delete=models.CASCADE,related_name='product_reviews')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='profile_reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='rating_between_1_and_5',
                check=Q(rating__gte=1, rating__lte=5),
                violation_error_message='Rating must be between 1 and 5.'
            )
        ]