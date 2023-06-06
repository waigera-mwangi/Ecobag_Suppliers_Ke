from django.shortcuts import render
from orders.models import Order
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from orders.models import Order, OrderItem
from finance.models import Payment
from django.http import HttpResponse
from supply.models import SupplyTender
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from accounts.models import Profile
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa


def checkout(request):
    user = User.objects.get(pk=1)
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
        payment_form = PaymentForm(request.POST)
        address_form = AddressForm(request.POST, instance=request.user)

        if payment_form.is_valid() and address_form.is_valid():
            transaction_id = payment_form.cleaned_data['transaction_id']
            # Check if a payment record already exists for the current order
            try:
                # save user address
                address = address_form.save(commit=False)
                address.user = request.user
                address.save()

                payment = Payment.objects.get(order=order)
                payment.transaction_id = transaction_id
                payment.payment_status = 'Pending'
                payment.save()
            except Payment.DoesNotExist:
                # enter data into payment model
                payment = Payment.objects.create(order=order, transaction_id=transaction_id,payment_status='pending',
                                                  town=address.town,county=address.county,phone_number=address.phone_number)
            
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
        address_form = PaymentForm()
        payment_form = AddressForm()
       
    context = {
        'payment_form': payment_form,
        'address_form':address_form,
        'order_OrderDeliveryFormtems': order_items,
        'order_total': order_total,
        
    }
    return render(request, 'finance/checkout.html', context)


def receipt(request, tender_id):
    tender = get_object_or_404(SupplyTender, id=tender_id, tender_status='Complete')

    receipt_data = {
        'transaction_id': tender.id,
        'username': tender.user.get_full_name,
        'quantity': tender.quantity,
        'total_cost': tender.total(),
        'payment_status': tender.tender_status,
        'date_tender': tender.date,
        'product': tender.product.name,
        'price': tender.price,
    }

    # Render the receipt HTML template
    receipt_html = render_to_string('finance/receipts/supplier-receipt.html', receipt_data)

    # Create a file-like buffer to receive PDF data
    pdf_buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    pisa_status = pisa.CreatePDF(receipt_html, dest=pdf_buffer)

    # Return the receipt PDF as a downloadable response
    if pisa_status.err:
        return HttpResponse('An error occurred: %s' % pisa_status.err)
    else:
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=Receipt_{tender.id}.pdf'
        return response
