from django.shortcuts import render
from .models import UserPickUpStation
from .forms import UserPickUpStationForm
from accounts.models import User
from django.urls import reverse_lazy
from orders.models import *
from .models import *
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
class UserPickUpStationCreateView(CreateView):
    model = UserPickUpStation
    form_class = UserPickUpStationForm
    template_name = 'orders/userpickupstation_form.html'
    success_url = reverse_lazy('store:view_cart')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def track_delivery(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        shipping = Shipping.objects.get(order=order)
    except (Order.DoesNotExist, Shipping.DoesNotExist):
        # handle the case where either the Cart or Shipping object does not exist
        return HttpResponseNotFound("Awaiting shipment")
    
    context = {
        'order': order,
        'shipping': shipping
    }
    
    return render(request, 'shipping/track_shipping.html', context)
