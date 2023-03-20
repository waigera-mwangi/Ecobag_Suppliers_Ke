
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from .forms import *
from django.shortcuts import get_object_or_404, render
import random

def create_supplyTender(request):
    form = SupplyTenderForm()
    if request.method == 'POST':
        form = SupplyTenderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Supply request made successfully")
            return redirect('supply:supply_request_list')
        else:
            messages.warning(request, "Error making request")
    context = {'form': form}
    return render(request, 'supply/request-supply.html', context)

def supply_request_list(request):
    user = request.user
    tender = SupplyTender.objects.filter()
    context = {"tender":tender}
    if user.user_type == 'RD':
        return render(request, "supply/supplier-request-list.html", context)
    else:
        return render(request, "supply/supply-request-list.html", context)


def delete_supply_request(request, pk):
    supply_request = SupplyTender.objects.get(id=pk)
    if request.method == 'POST':
        supply_request.delete()
        messages.success(request, "Request removed successfully")
        return redirect('supply:supply_request_list')
    context = {"supply_request":supply_request}
    return render(request, 'supply/delete_request.html', context)

def update_supply_request(request, pk):
    supply_request = SupplyTender.objects.get(id=pk)
    form = SupplyTenderForm(instance=supply_request)

    if request.method == 'POST':
        form = SupplyTenderForm(request.POST, instance=supply_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Request updated successfully")
            return redirect('supply:supply_request_list')
        else:
            messages.warning(request, "Error updating request")
    context = {"form":form}
    return render(request, 'supply/update-request.html',context)

def create_supply(request):
    form = SupplyForm()
    if request.method == 'POST':
        form = SupplyForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = request.user
            user.save()
            form.save()
            messages.success(request, "Supply made successfully")
            return redirect('supply:supply_request_list')
        else:
            messages.warning(request, "Error making supply")
    context = {'form': form}
    return render(request, 'supply/create-supply.html', context)

def supply_list(request):
    supply = ProductSupply.objects.filter()
    context = {'supply':supply}
    return render(request, "supply/supply-list.html", context)
    
