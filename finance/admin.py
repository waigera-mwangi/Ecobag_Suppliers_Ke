from django.contrib import admin
from .models import *


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'payment_status', 'payment_date')


    def user(self, obj):
    	return obj.order.user




admin.site.register(Payment, PaymentAdmin)

# Register your models here.
