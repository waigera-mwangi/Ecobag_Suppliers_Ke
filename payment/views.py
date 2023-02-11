import stripe

from django.shortcuts import render
from basket.basket import Basket

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