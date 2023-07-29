from django.contrib import admin

from .models import Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ('order_tno','user','brand_name','brand_logo', 'created',)
    list_filter = ('created','user','brandstatus')
    search_fields = ('id','user_username')
    # readonly_fields = ('created', 'brand_logo')
    
    def order_tno(self, obj):
        return obj.brand.order_tno
    
    def download_logo(self, obj):
        if obj.brand_logo:
            return '<a href="{}" download>Download</a>'.format(obj.brand_logo.url)
        return 'No logo available'

    download_logo.allow_tags = True
    download_logo.short_description = 'Logo Download'
    

admin.site.register(Brand, BrandAdmin)