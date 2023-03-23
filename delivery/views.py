from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import *
from .forms import *

# Delivery views

def create_delivery(request):
    form = DeliveryForm()
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Delivery created successfully")
            return redirect('delivery:delivery_list')
        else:
            messages.warning(request, "Error creating delivery")
    context = {'form': form}
    return render(request, 'delivery/create-delivery.html', context)

# view delivery list
def delivery_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    list_delivery = Delivery.objects.filter()
    context = {"list_delivery":list_delivery}
    return render(request,"delivery/list_delivery.html",context)

# view delivery list
def delivery_list_driver(request):
    if not request.user.is_authenticated:
        return redirect('login')
    list_delivery = Delivery.objects.filter()
    context = {"list_delivery":list_delivery}
    return render(request,"delivery/list_delivery_driver.html",context)


# delete delivery
def delete_delivery(request, pk):
    order = Delivery.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('delivery:delivery_list')
    context = {"order":order}
    return render(request, 'delivery/delete_delivery.html', context)

def update_delivery(request, pk):
    delivery = Delivery.objects.get(id=pk)
    form = DeliveryForm(instance=delivery)

    if request.method == 'POST':
        form = DeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            form.save()
            messages.success(request, "Delivery updated successfully")
            return redirect('delivery:delivery_list')
        else:
            messages.warning(request, "Error updating delivery")
    context = {"form":form}
    return render(request, 'delivery/create-delivery.html',context)

def update_delivery_driver(request, pk):
    delivery = Delivery.objects.get(id=pk)
    form = DeliveryForm(instance=delivery)

    if request.method == 'POST':
        form = DeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            form.save()
            messages.success(request, "Delivery updated successfully")
            return redirect('delivery:delivery_list_driver')
        else:
            messages.warning(request, "Error updating delivery")
    context = {"form":form}
    return render(request, 'delivery/create_delivery_driver.html',context)

