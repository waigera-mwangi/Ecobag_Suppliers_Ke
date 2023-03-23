from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from basket.basket import Basket
from .models import *
from store.models import Product
from django.contrib import messages
import random
from .forms import OrderForm

# imports for invoice

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# invoice
def orders_pdf(request):
    # bytestream buffer
    buf = io. BytesIO()
    # canva
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # textobject
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)

    orderitems = Order.objects.filter(user=request.user)
    
    # blan list
    lines = [
        "Ecobag Suppliers ke",
        "Invoice",
        "---------------------------------------------------",

    ]
    

    for orderitem in orderitems:
        lines.append("First Name: " + orderitem.fname)
        lines.append("Last Name: " + orderitem.lname)
        lines.append("Phone: " + str(orderitem.phone))
        lines.append("Email: " + orderitem.email)
        lines.append("Tracking no: " + orderitem.tracking_no)
        lines.append("Amount Paid: " + orderitem.amount_paid)
        lines.append("Status: " + orderitem.orderstatus)
        lines.append("======================")

    # blan list
    lines = [
        "Thank you for being part of us",
        "---------------------------------------------------",

    ]

    # loop
    for line in lines:
        textob.textLine(line)

    
    # finish
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='invoice.pdf')

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

    return redirect('store:view-product')

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

# customer to view orders in table
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


# staff to view orders in table

def orders_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    list_orders = Order.objects.filter()
    context = {"list_orders":list_orders}
    return render(request,"orders/orders_list.html",context)


# create order
def create_order(request):

    form =  OrderForm()
    if request.method == 'POST':
        form =  OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Order created successfully")
            return redirect('order:orders_list')
        else:
            messages.warning(request, "Error creating order")
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
            return redirect('orders:orders_list')
        else:
            messages.warning(request, "Error updating order")
    context = {"form":form}
    return render(request, 'orders/create_order.html',context)

# delete order
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Delivery deleted succesfully")
        return redirect('orders:orders_list')
    else:
            messages.warning(request, "Error while deleting delivery")

    context = {"order":order}
    return render(request, 'orders/delete_order.html', context)

# dispatch manager view approved orders
def orders_approved(request):
    if not request.user.is_authenticated:
        return redirect('login')
    list_orders = Order.objects.filter(orderstatus='Approved')
    context = {"list_orders":list_orders}
    return render(request,"orders/orders_approved.html",context)

# driver view approved orders
def update_order_driver(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order updated successfully")
            return redirect('orders:orders_list')
        else:
            messages.warning(request, "Error updating order")
    context = {"form":form}
    return render(request, 'orders/create_order_driver.html',context)

# driver view orders in table
def orders_list_driver(request):
    if not request.user.is_authenticated:
        return redirect('login')
    list_orders = Order.objects.filter(orderstatus='Approved')
    context = {"list_orders":list_orders}
    return render(request,"orders/orders_list_driver.html",context)
