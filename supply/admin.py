from django.contrib import admin

from .models import *


class ProductSupplyAdmin(admin.ModelAdmin):
    list_display =('item','quantity','created_date','supply_status')

class SupplyTenderAdmin(admin.ModelAdmin):
    list_display =('item','quantity','created_date','tender_status')

admin.site.register(ProductSupply,ProductSupplyAdmin)
admin.site.register(SupplyTender, SupplyTenderAdmin)