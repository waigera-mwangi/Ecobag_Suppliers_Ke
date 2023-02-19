from django.contrib import admin

from .models import (
    # Customer,
    Product,
    Category
)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'price', 'quantity', 'created_date', 'description')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')


# admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

