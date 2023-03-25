from django.contrib import admin
from .models import Order
from .models import OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transaction_id', 'is_completed', 'date_ordered')
    list_filter = ('date_ordered', 'is_completed')
    search_fields = ('id', 'user__username')
    readonly_fields = ('date_ordered',)

    def transaction_id(self, obj):
        return obj.payment.transaction_id


admin.site.register(Order, OrderAdmin)
