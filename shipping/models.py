from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from orders.models import Order


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PickUpStation(models.Model):
    name = models.CharField(max_length=50)
    # users = models.ManyToManyField(User, related_name='pickup_stations')
    description = models.TextField(max_length=255, null=True)
    location = models.ForeignKey(Location, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserPickUpStation(models.Model):
    user = models.ForeignKey(User, related_name='pick_up_stations', on_delete=models.CASCADE)
    station = models.ForeignKey(PickUpStation, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    # other fields for UserPickUpStation model


    def __str__(self):
        return f"{self.station.name} ({self.station.location.name})"

        
    def description(self):
        return self.station.description


   
class Shipping(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PD', _('Pending')
        OUT_FOR_DELIVERY = 'OFD', _('Out For Delivery')
        DELIVERED = 'DL', _('Delivered')

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField(auto_now_add=True, verbose_name='shipped_date')
    station = models.ForeignKey(UserPickUpStation, on_delete=models.CASCADE, null=True)
    status = models.CharField(_('status'), max_length=3, choices=Status.choices, default=Status.PENDING)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipments_as_driver')
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipments_as_service_provider', null=True)

    def __str__(self):
        return f'Shipping #{self.id}'

    def get_status_display(self):
        return dict(Shipping.Status.choices)[self.status]