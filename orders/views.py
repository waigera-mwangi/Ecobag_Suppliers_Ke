from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from basket.basket import Basket
from .models import Order,OrderItem
from store.models import Product
from django.contrib import messages
import random
from .forms import OrderForm
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
        
        trackno = 'order'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'order'+str(random.randint(1111111,9999999))
        neworder.tracking_no = trackno
        neworder.save()
        
       

        for item in basket:
            OrderItem.objects.create(
                order=neworder,
                product=item['product'],
                price=item['price'],
                quantity=item['qty']
            )
        
        
        # decrease product qty from stock 
        # orderproduct = Product.objects.filter(id=item.product_id).first()
        # orderproduct.quantity = orderproduct.quantity - item.product_qty
        # orderproduct.save()

        # clear cart
        basket.clear()
        messages.success(request, 'Order placed Successfully. ')

    return redirect('/')

# checking if the product exists before making orders 
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

# customer to view ordersin table
def view_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    currentuser=request.user.email
    orders = Order.objects.filter(email=currentuser)
    status=Order.objects.filter()
    context = {"orders":orders, "status":status}
    return render(request,"orders/view-orders.html",context)

# view single order by customer
def order_view(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order':order, 'orderitems':orderitems}
    return render(request,"orders/orderview.html", context)


# staff to view ordersin table

def orders_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter()
    status=Order.objects.filter()
    context = {"orders":orders, "status":status}
    return render(request,"orders/orders_list.html",context)


# create order
def create_order(request):

    form =  OrderForm()
    if request.method == 'POST':
        form =  OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Order updated successfully")
            return redirect('store:order_list')
        else:
            messages.warning(request, "Error updating order")
    context ={"form":form}
    return render(request, 'orders/create_order.html',context)

# update order
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order updated successfully")
            return redirect('accounts:finance_manager')
        else:
            messages.warning(request, "Error updating order")
    context = {"form":form}
    return render(request, 'orders/create_order.html',context)

# delete order
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {"order":order}
    return render(request, 'orders/delete_order.html', context)