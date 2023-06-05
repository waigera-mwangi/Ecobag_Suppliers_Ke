from django.db import models
from decimal import Decimal
from django.conf import settings
from accounts.models import User
from store.models import Product
from phonenumber_field.modelfields import PhoneNumberField

class CustomPhoneNumberField(PhoneNumberField):
    default_error_messages = {
        'invalid': 'Please enter a valid phone number in the format +254723000000.',
    }


class Order(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = CustomPhoneNumberField(null=True)
    county = models.CharField(max_length=20,null=True)
    town = models.CharField(max_length=20,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date ordered')
    is_completed = models.BooleanField(default=False)  
    products = models.ManyToManyField(Product, through='OrderItem')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart for {self.order.user.username}"

    def subtotal(self):
        return self.product.price * self.quantity
