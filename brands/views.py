from django.shortcuts import render, redirect
from .models import Brand
from orders.models import Order
from django.contrib import messages
import random


def custom_branding(request):
    if not request.user.is_authenticated:
        return redirect('login')
    currentuser=request.user.email
    return render(request, 'brands/custom_branding.html')



def branding(request):
    if request.method == 'POST':
        newbrand = Brand()
        newbrand.user = request.user
        newbrand.brand_name  = request.POST.get('brand_name')
        newbrand.brand_logo  = request.POST.get('brand_logo')
        newbrand.order_tno  = request.POST.get('t_no')
      
        trackingno = 'brand'+str(random.randint(1111111,9999999))
        while Brand.objects.filter(brand_tno=trackingno) is None:
            trackingno = 'brand'+str(random.randint(1111111,9999999))
        newbrand.brand_tno = trackingno

        newbrand.save()

        messages.success(request, 'Submitted successfully for branding')
        
    return redirect('/')