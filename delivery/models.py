from django.db import models

from orders.models import *

class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    driver_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    status = (
        ('Pending','Pending'),
        ('Shiping in progress','Shipping in progress'),
        ('Completed','Completed'),
    )
    deliverystatus = models.CharField(max_length=50, choices=status, default='Pending')
    class Meta:
        verbose_name_plural = 'Deliveries'

    def __str__(self):
        return self.order


