from django.db import models
from accounts.models import User
from orders.models import Order
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Payment(models.Model):
    class Meta:
        verbose_name = 'Order Payment'
        verbose_name_plural = 'Order Payments'

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='Pending')
