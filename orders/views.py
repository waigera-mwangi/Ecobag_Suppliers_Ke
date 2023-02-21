from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.http import HttpResponse
from basket.basket import Basket
from .models import Order, OrderItem
from store.models import Product
from django.contrib import messages
# new views

def placeorder(request):
    basket = Basket(request)
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.county = request.POST.get('county')
        neworder.town = request.POST.get('town')
        neworder.mpesa_code = request.POST.get('mpesa_code')

        neworder.amount_paid = basket.get_total_price()

        neworder.save()
        # decrease product qty
       
        # clear cart
        basket.clear()
        # return HttpResponse("Order successful")
        messages.success(request, 'Order placed Successfully.')


    return redirect('/')

# my views
def checkout(request):
    data = {}
    try:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
       
        products = []
        for item in order.orderitem_set.all():
            product = {
                'quantity': item.quantity,
                'name': item.product.name,
                'slug': item.product.slug,
            }
            products.append(product)
        print(products)
        for item in products:
            product = Product.objects.filter(slug=item['slug']).first()
            if product.quantity >= item['quantity']:
                print(f"{product.quantity} >= {item['quantity']}")
                print("Everything is fine products exists")
            else:
                instance = OrderItem.objects.get(order=order, product=product)
                if product.quantity > 0:
                    instance.quantity = product.quantity
                    instance.save()
                else:
                    instance.delete()
    except AttributeError:
        pass
    return render(request, 'orders/checkout.html')

# view orders
def view_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    currentuser=request.user.username
    items = Order.objects.filter(email=currentuser)
    status=Order.objects.filter()
    context = {"items":items, "status":status}
    return render(request,"orders/view-orders.html",context)

