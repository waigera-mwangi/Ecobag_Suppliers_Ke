import stripe
import json

from django.shortcuts import render
from basket.basket import Basket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.views import payment_confirmation

def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total =  total.replace('.', '')
    total = int(total)
    
    stripe.api_key = 'sk_test_51MZvCeJh1JJwaJ0btlGhnoOmlccrmTi0L5daGLr7tCKuFMdpsLzCa2HAuYlbW5FiiLPmOonyFETCRFnXA39Yqqfo000rF8d1rA'
    intent =  stripe.PaymentIntent.create(
        amount = total,
        currency = 'gbp',
        metadata={'userid': request.user.id}
    )
    return render(request, 'payment/checkoutform.html',{'client_secret': intent.client_secret})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type{}'.format(event.type))

    return HttpResponse(status=200)

def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')
    