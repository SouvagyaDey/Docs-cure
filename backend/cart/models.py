from django.db import models
from authy.models import Profile
from products.models import ProductStore
import uuid

# Cart model
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile_cart')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Cart {self.id} for {self.profile.user.email}"



class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(ProductStore, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('cart', 'product')
        ordering = ['-created_at']

        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0),
                name='quantity_gt_0'
            )
        ]


    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"