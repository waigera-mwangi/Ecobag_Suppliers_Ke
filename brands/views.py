from django.shortcuts import render, redirect
from .models import Brand
from orders.models import Order
from django.contrib import messages
from .forms import *
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
        
    return redirect('brands:view_brands')

# staff to view brands in table
def brand_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    list_brands = Order.objects.filter()
    context = {"list_brands":list_brands}
    return render(request,"brands/brands_list.html",context)

# staff create brand
def create_brand(request):

    form =  BrandForm()
    if request.method == 'POST':
        form =  BrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Order created successfully")
            return redirect('brands:brand_list')
        else:
            messages.warning(request, "Error creating order")
    context ={"form":form}
    return render(request, 'brands/create_brand.html',context)

# update brand
def update_brand(request, pk):
    brand = Order.objects.get(id=pk)
    form = BrandForm(instance=brand)

    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand updated successfully")
            return redirect('brands:brand_list')
        else:
            messages.warning(request, "Error updating brand")
    context = {"form":form}
    return render(request, 'brands/create_brand.html',context)

# staff delete brand
def delete_brand(request, pk):
    brand = Brand.objects.get(id=pk)
    if request.method == 'POST':
        brand.delete()
        return redirect('brands:brand_list')
    context = {"brand":brand}
    return render(request, 'brands/delete_brand.html', context)

# customer to view brands in table
def view_brands(request):
    if not request.user.is_authenticated:
        return redirect('login')
    currentuser = request.user
    brands = Brand.objects.filter(user = currentuser)
    context = {'brands':brands}
    return render(request,"brands/view-brands.html",context)