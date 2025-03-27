from django.db import models
from django.contrib.auth.models import User
import uuid


# ✅ Model sản phẩm
class Product(models.Model):
    UNIT_CHOICES = [
        ('qty', 'Quantity'),
        ('container', 'Container'),
    ]
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True, editable=False)    
    name = models.CharField(max_length=255)
    available_at_store = models.BooleanField(default=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='qty', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ✅ Model lưu đơn đặt hàng của từng nhân viên
class OrderEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_entries")
    order_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    is_processed = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.staff.username} đặt {self.order_quantity} x {self.product.name}"
