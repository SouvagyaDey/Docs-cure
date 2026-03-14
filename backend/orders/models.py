from django.db import models
from authy.models import Profile
import uuid
from django.db.models import Sum
from products.models import ProductStore

class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    shipping_address = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return f"Order {self.id} - {self.profile.user} ({self.status})"


    def update_total(self):
        total = self.order_items.aggregate(Sum("subtotal"))["subtotal__sum"] or 0
        self.total_amount = total
        self.save(update_fields=["total_amount"])



class OrderItem(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(ProductStore, on_delete=models.CASCADE, related_name="product_items")
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total()


    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.order.update_total()


    def __str__(self):
        return f"{self.product.name} x {self.quantity}"