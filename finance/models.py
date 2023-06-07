from django.db import models
from accounts.models import User
from orders.models import Order
from phonenumber_field.modelfields import PhoneNumberField

class CustomPhoneNumberField(PhoneNumberField):
    default_error_messages = {
        'invalid': 'Please enter a valid phone number in the format +254723000000.',
    }

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
    county = models.CharField(null=True, max_length=100)
    town = models.CharField(null=True, max_length=100)
    phone_number = CustomPhoneNumberField(null=True, unique=True)
