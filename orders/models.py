from django.db import models
from decimal import Decimal
from django.conf import settings

from store.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    fname = models.CharField(max_length=20)
    lname  = models.CharField(max_length=20)
    phone = models.IntegerField(default=0)
    email = models.CharField(max_length=50)
    county = models.CharField(max_length=20)
    town = models.CharField(max_length=20)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    mpesa_code = models.CharField(max_length=8,)
    amount_paid = models.CharField(max_length=250)
    tracking_no = models.CharField(max_length=150)
    status = (
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        ('Out for shipping','Out for shipping'),
        ('Completed','Completed'),
    )
    orderstatus = models.CharField(max_length=50, choices=status, default='Pending')

    # class Meta:
    #     ordering = ('-created',)

    def __str__(self):
        return '{} - {}'.format(self.id,self.tracking_no)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    quantity = models.PositiveBigIntegerField(default=1)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} {}'.format(self.order.id,self.order.tracking_no)
