from django.shortcuts import render
from orders.models import Order

# def finance_home(request):
#     orders = Order.objects.all()
#     total_orders = orders.count()
#     pending = orders.object.filter(orderstatus='Pending').count()
#     completed = orders.object.filter(orderstatus='Completed').count()

#     context = {'orders':orders,
#               'total_orders':total_orders,
#               'pending':pending,
#               'completed':completed}
    
#     return render(request, 'finance-manager.html', context)