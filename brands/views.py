from django.shortcuts import render, redirect,get_object_or_404
from .models import Brand
from django.contrib import messages
from .forms import *
from finance.models import Payment
import random
from django.core.exceptions import ObjectDoesNotExist

#  customer crete brand with the transaction id 
def branding(request):
    form = BrandForm()
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.save(commit=False)
            
            transaction_id = brand.order_tno
            user = request.user
            
            try:
                payment = Payment.objects.get(order__user=user, transaction_id=transaction_id)
                
                if payment.payment_status != 'Approved':
                    messages.warning(request, "No matching approved payment found for the provided transaction ID.")
                    return redirect('brands:brand_list')
                
                brand.user = user
                brand.save()
                
                messages.success(request, "Brand created successfully")
                return redirect('brands:view_brands')
            
            except Payment.DoesNotExist:
                messages.warning(request, "No matching payment found for the provided transaction ID.")
                return redirect('brands:branding')
            
        else:
            messages.warning(request, "Error creating brand")
    
    context = {"form": form}
    return render(request, 'brands/create_brand.html', context)

# customer to view brands in table
def view_brands(request):
    if not request.user.is_authenticated:
        return redirect('login')
    currentuser = request.user
    brands = Brand.objects.filter(user = currentuser)
    context = {'brands':brands}
    return render(request,"brands/view-brands.html",context)

# staff to view brands in table
def brand_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    list_brands = Brand.objects.filter()
    context = {"list_brands":list_brands}
    return render(request,"brands/brands_list.html",context)

# staff create brand
def create_brand(request):
    form =  BrandForm()
    if request.method == 'POST':
        form =  BrandForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.save(commit=False) # Save the form data without committing to the database yet
            
            # Check if the transaction_id exists in the Payment model for the current user
            transaction_id = brand.order_tno
            user = request.user
            payment = get_object_or_404(Payment, order__user=user, transaction_id=transaction_id)
            
            if payment.payment_status != 'approved':
                messages.warning(request, "No matching approved payment found for the provided transaction ID.")
                return redirect('brands:brand_list')
            # Associate the brand with the current user and save it
            brand.user = user
            brand.save()
            
            messages.success(request, "Brand created successfully")
            return redirect('brands:brand_list')
        else:
            messages.warning(request, "Error creating brand")
    context ={"form":form}
    return render(request, 'brands/create_brand.html',context)

# update brand
def update_brand(request, pk):
    print(pk)
    brand = Brand.objects.get(id=pk)
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



def brand_view(request, brand_id):
    if not request.user.is_authenticated:
        return redirect('/')
    brand = get_object_or_404( Brand, id = brand_id)
    return render(request, 'brands/brand_view.html', {'brand': brand})