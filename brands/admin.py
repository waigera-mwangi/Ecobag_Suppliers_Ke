from django.contrib import admin

from .models import Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ('order_tno','user','brand_name', 'created')
    list_filter = ('created','user','brandstatus')
    search_fields = ('id','user_username')
    readonly_fields = ('created', 'brand_logo')
    
    def order_tno(self, obj):
        return obj.brand.order_tno

admin.site.register(Brand, BrandAdmin)