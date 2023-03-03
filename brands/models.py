from django.db import models
from orders.models import Order
from django.conf import settings

class Brand(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='brand_user')
    order_tno = models.CharField(max_length=150)
    brand_tno = models.CharField(max_length=150)
    brand_name = models.CharField(max_length=20)
    brand_logo = models.ImageField(upload_to='media/%Y/%m/%d/', blank=True)
