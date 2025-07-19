from django.db import models
from django.contrib.auth import get_user_model
from services.models import Service

User = get_user_model()

class Order(models.Model):
    PENDING = 'pending'
    PAID = 'paid'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Ожидает оплаты'),
        (PAID, 'Оплачен'),
        (DELIVERED, 'Доставлен'),
        (CANCELLED, 'Отменен'),
    ]
    
    PAYMENT_ONLINE = 'online'
    PAYMENT_COURIER = 'courier'
    PAYMENT_CHOICES = [
        (PAYMENT_ONLINE, 'Онлайн оплата'),
        (PAYMENT_COURIER, 'Оплата курьеру'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.service.title} in order #{self.order.id}"