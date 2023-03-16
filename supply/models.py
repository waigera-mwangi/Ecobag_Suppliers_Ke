from django.db import models
from decimal import Decimal
from django.conf import settings

class ProductSupply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='supplied')
    item = models.CharField(max_length=255)
    quantity = models.IntegerField()
    created_date = models.DateField(auto_now=True)
    price = models.IntegerField(default=500)
    status = (
        ('Pending','Pending'),
        ('Complete','Complete'),
    )
    supply_status = models.CharField(max_length=50, choices=status, default='Pending')

    class Meta:
        verbose_name_plural = 'Product Supplies'
    
    def __str__(self):
        return self.item

class SupplyTender(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='needs_supply')
    item = models.CharField(max_length=255)
    quantity = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(('Updated'), auto_now=True, null=True)
    
    status = (
        ('Pending','Pending'),
        ('Complete','Complete'),
    )
    tender_status = models.CharField(max_length=50, choices=status, default='Pending')

    class Meta:
        verbose_name_plural = 'Supply Tenders'
    
    def __str__(self):
        return self.item
