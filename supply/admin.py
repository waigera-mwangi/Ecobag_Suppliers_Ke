from django.contrib import admin

from .models import *


class SupplyTenderAdmin(admin.ModelAdmin):
    list_display =('product','quantity','date','tender_status')


admin.site.register(SupplyTender, SupplyTenderAdmin)