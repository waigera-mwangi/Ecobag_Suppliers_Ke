from django.contrib import admin

from .models import (
    # Customer,
    Product,
    Order,
    Delivery,
    Category
)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'price', 'quantity', 'created_date', 'description')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'completed','is_active', 'is_archived', 'created_date', 'updated')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','')


# admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Delivery)
