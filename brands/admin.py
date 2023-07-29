from django.contrib import admin
from django.utils.html import format_html
from .models import Brand

class BrandAdmin(admin.ModelAdmin):
    list_display = ('order_tno', 'user', 'brand_name', 'created', 'preview_logo')  # Add 'preview_logo'

    list_filter = ('created', 'user', 'brandstatus')
    search_fields = ('id', 'user__username')  # Correct the search field for the user's username
    
    def order_tno(self, obj):
        return obj.order_tno
    
    def preview_logo(self, obj):
        if obj.brand_logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.brand_logo.url)
        return 'No logo available'

    preview_logo.allow_tags = True
    preview_logo.short_description = 'Logo Preview'
    

admin.site.register(Brand, BrandAdmin)
