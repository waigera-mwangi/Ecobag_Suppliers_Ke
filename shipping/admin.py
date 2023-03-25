from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from .models import Location, PickUpStation, UserPickUpStation, Shipping
from  orders.models import Order



class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at',)
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at',)


class PickUpStationAdmin(admin.ModelAdmin):
    list_display = ( 'location', 'created_at', 'updated_at',)
    list_filter = ('created_at', 'updated_at',)
    search_fields = ()
    readonly_fields = ('created_at', 'updated_at',)


class UserPickUpStationAdmin(admin.ModelAdmin):
    list_display = ('user', 'station', 'location', 'created_at', 'updated_at',)
    list_filter = ('created_at', 'updated_at', 'station')
    search_fields = ('user', 'station',)
    readonly_fields = ('created_at', 'updated_at',)

    def location(self, obj):
        return obj.station.location.name


class ShippingAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'delivery_date', 'station', 'status', 'driver',)
    list_filter = ('delivery_date', 'station',)
    search_fields = ('name', 'order')
    readonly_fields = ('delivery_date',)

    # def transaction_id(self, obj):
    #     return obj.order.transaction_id


admin.site.register(Location, LocationAdmin)
admin.site.register(PickUpStation, PickUpStationAdmin)
admin.site.register(UserPickUpStation, UserPickUpStationAdmin)
admin.site.register(Shipping, ShippingAdmin)