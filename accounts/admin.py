from django.contrib import admin
from .models import User
from .models import Profile

admin.site.site_header = "Ecobag Suppliers ke, ADMIN "
admin.site.site_title = "Ecobag Suppliers ke "
admin.site.index_title = "Ecobag Suppliers ke"
admin.site.register(User)

# class ProfileAdmin(admin.ModelAdmin):
#     list_display('name','image', 'gender')

admin.site.register(Profile)

