
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from .forms import *
from django.shortcuts import get_object_or_404, render

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

def create_supply(request):
    form = SupplyForm()
    if request.method == 'POST':
        form = SupplyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Supply made successfully")
            return redirect('supply:supply_request_list')
        else:
            messages.warning(request, "Error making supply")
    context = {'form': form}
    return render(request, 'supply/create-supply.html', context)


def supply_request_list(request):
    tender = SupplyTender.objects.filter()
    context = {"tender":tender}
    return render(request, "supply/supply-request-list.html", context)