from django.db import models
from django.conf import settings

class Brand(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='brand_user')
    created = models.DateField(auto_now_add=True)
    order_tno = models.CharField(max_length=150)
    brand_tno = models.CharField(max_length=150)
    brand_name = models.CharField(max_length=20)
    brand_logo = models.ImageField(null=True)
    
    
    status = (
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        ('Completed','Completed'),
    )
    
    brandstatus = models.CharField(max_length=50, choices=status, default='Pending')

    def __str__(self):
        return '{}'.format(self.brand_tno)