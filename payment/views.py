import json

from django.shortcuts import render
from basket.basket import Basket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from orders.views import payment_confirmation

# def BasketView(request):
#     basket = Basket(request)
#     total = str(basket.get_total_price())
#     total =  total.replace('.', '')
#     total = int(total)
    
#     stripe.api_key = 'sk_test_51MZvCeJh1JJwaJ0btlGhnoOmlccrmTi0L5daGLr7tCKuFMdpsLzCa2HAuYlbW5FiiLPmOonyFETCRFnXA39Yqqfo000rF8d1rA'
#     intent =  stripe.PaymentIntent.create(
#         amount = total,
#         currency = 'gbp',
#         metadata={'userid': request.user.id}
#     )
#     return render(request, 'payment/checkout.html',{'client_secret': intent.client_secret})

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     event = None

#     try:
#         event = stripe.Event.construct_from(
#             json.loads(payload), stripe.api_key
#         )
#     except ValueError as e:
#         print(e)
#         return HttpResponse(status=400)

#     if event.type == 'payment_intent.succeeded':
#         payment_confirmation(event.data.object.client_secret)

#     else:
#         print('Unhandled event type{}'.format(event.type))

#     return HttpResponse(status=200)

# def order_placed(request):
#     basket = Basket(request)
#     basket.clear()
#     return render(request, 'payment/orderplaced.html')
    

# my views


# def checkout(request):
#     basket = Basket.objects.filter(user=request.user)
#     for item in basket:
#         if item.qty > item.product.quantity:
#            Basket.objects.delete(id=item.id)
    

#     basket = Basket.objects.filter(user=request.user)
    
#     for item in basket:
#         total = str(basket.get_total_price())
#         total =  total.replace('.', '')
#         total = int(total)

#     context = {'basketitems':basket, 'total_price':total}
#     return render(request, "store/checkout.html", context)


# def checkout(request):
#     data = {}
#     try:
#         customer = request.user.customer
#         order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
#         data['order'] = order
#         data['form'] = OrderPaymentForm
#         data['object_list'] = order.orderitem_set.all()
#         products = []
#         for item in order.orderitem_set.all():
#             product = {
#                 'quantity': item.quantity,
#                 'name': item.product.name,
#                 'slug': item.product.slug,
#             }
#             products.append(product)
#         print(products)
#         for item in products:
#             product = Product.objects.filter(slug=item['slug']).first()
#             if product.quantity >= item['quantity']:
#                 print(f"{product.quantity} >= {item['quantity']}")
#                 print("Everything is fine products exists")
#             else:
#                 instance = OrderItem.objects.get(order=order, product=product)
#                 if product.quantity > 0:
#                     instance.quantity = product.quantity
#                     instance.save()
#                 else:
#                     instance.delete()
#     except AttributeError:
#         pass
#     return render(request, 'store/checkout.html', data)


# def checkout_pay(request):
#     data = {}
#     customer = request.user.customer
#     order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
#     if request.method == "POST":
#         form = OrderPaymentForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             mpesa = instance.mpesa
#             if len(mpesa) == 10:
#                 if instance.amount == order.get_cart_total:
#                     instance.order = order
#                     instance.transaction_id = generate_key(8, 8)
#                     instance.save()
#                     data['message'] = "Payment has been done successfully"
#                     order.completed = True
#                     order.save()
#                     items = order.orderitem_set.all()
#                     for item in items:
#                         product = Product.objects.filter(id=item.product.id).first()
#                         quantity = product.quantity - item.quantity
#                         product.quantity = quantity
#                         product.save()
#                 else:
#                     data['info'] = f"amount sent is {instance.amount} but amount required is {order.get_cart_total}"
#             else:
#                 data['mpesa'] = "Enter valid mpesa code"
#         else:
#             data['info'] = "This form is invalid"
#             data['form'] = form.errors
#     return JsonResponse(data)


# def order_list(request):
#     data = {}
#     customer = request.user.customer
#     order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
#     data['order'] = order
#     return render(request, 'store/checkout.html', data)
