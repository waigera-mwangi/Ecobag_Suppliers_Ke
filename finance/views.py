from django.shortcuts import render
from orders.models import Order
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PaymentForm
from orders.models import Order, OrderItem
from finance.models import Payment



def checkout(request):
    user = User.objects.get(pk=1)
    pick_up_stations = user.pick_up_stations.all()
    order_items = OrderItem.objects.all()


    # Get the latest pending order for the logged-in user
    try:
        order = Order.objects.filter(user=request.user, is_completed=False).latest('id')
    except Order.DoesNotExist:
        messages.error(request, 'Your order is empty.')
        return redirect('store:product-view')

    
    order_items = order.orderitem_set.all()
    order_total = sum([item.subtotal() for item in order_items])



    # Create a Customer object for the user if it does not exist already
    try:
        customer = request.user
    except ObjectDoesNotExist:
        customer = User.objects.create(user=request.user)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            transaction_id = form.cleaned_data['transaction_id']
            # Check if a payment record already exists for the current order
            try:
                payment = Payment.objects.get(order=order)
                payment.transaction_id = transaction_id
                payment.payment_status = 'Pending'
                payment.save()
            except Payment.DoesNotExist:
                payment = Payment.objects.create(order=order, transaction_id=transaction_id, payment_status='pending')
            
            # Update product quantity in stock
            for item in order_items:
                product = item.product
                if product.quantity >= item.quantity:
                    product.quantity -= item.quantity
                    if product.quantity < 0: # check if the updated quantity is a positive integer
                        messages.error(request, f"{product.name} is out of stock.")
                        return redirect('store:view_cart')
                    product.save()
                else:
                    messages.error(request, f"{product.name} is out of stock.")
                    return redirect('store:view_cart')

            # Set the order as completed
            order.is_completed = True
            order.save()

            messages.success(request, 'Payment was successful!')
            return redirect('store:view_cart')
    else:
        form = PaymentForm()

    userpickupstations = customer.pick_up_stations.all()

    context = {
        'form': form,
        'order_items': order_items,
        'order_total': order_total,
        'userpickupstations': userpickupstations
    }
    return render(request, 'orders/checkout.html', context)
