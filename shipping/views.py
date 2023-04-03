from django.shortcuts import render
from .models import *
from .forms import *
from accounts.models import User
from django.urls import reverse_lazy
from orders.models import *
from django.shortcuts import redirect
from django.views.generic import View
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


class PickUpStationCreateView(CreateView):
    model = PickUpStation
    form_class = PickUpStationForm
    template_name = 'shipping/pickupstation_form.html'
    success_url = reverse_lazy('shipping:pickupstation_list')


class PickUpStationUpdateView(UpdateView):
    model = PickUpStation
    form_class = PickUpStationForm
    template_name = 'shipping/pickupstation_update.html'
    success_url = reverse_lazy('shipping:pickupstation_list')


class PickUpStationListView(ListView):
    model = PickUpStation
    template_name = 'shipping/pickupstation_list.html'
    context_object_name = 'pickupstations'


class PickUpStationDetailView(DetailView):
    model = PickUpStation
    template_name = 'shipping/pickupstation_detail.html'
    context_object_name = 'pickupstation'


class ServiceDeliveredListView(ListView):
    model = Shipping
    template_name = 'shipping/Service_delivered_shipping_list.html'
    context_object_name = 'shipping_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == user.UserTypes.DISPATCH_MANAGER:
            return Shipping.objects.filter(status__in=[Shipping.Status.DELIVERED])
        return super().get_queryset()

class DriverShippingListView(ListView):
    model = Shipping
    template_name = 'shipping/driver_shipping_list.html'
    context_object_name = 'shipping_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == user.UserTypes.DRIVER:
            return Shipping.objects.filter(driver=user, status=Shipping.Status.PENDING)
        return super().get_queryset()


class OutForDeliveryListView(ListView):
    model = Shipping
    template_name = 'shipping/driver_out_shipping_list.html'
    context_object_name = 'shipping_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == user.UserTypes.DRIVER:
            return Shipping.objects.filter(driver=user, status__in=[Shipping.Status.OUT_FOR_DELIVERY])
        return super().get_queryset()

class DeliveredListView(ListView):
    model = Shipping
    template_name = 'shipping/driver_delivered_shipping_list.html'
    context_object_name = 'shipping_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == user.UserTypes.DRIVER:
            queryset = Shipping.objects.filter(driver=user, status=Shipping.Status.DELIVERED)
            return queryset
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userpickupstations'] = UserPickUpStation.objects.all()
        return context

class UpdateShippingStatusView(View):
    def post(self, request, pk):
        shipping = Shipping.objects.get(pk=pk)
        if shipping.driver != request.user:
            return redirect('shipping:driver-shipping-list')

        status = request.POST.get('status')
        if status == Shipping.Status.OUT_FOR_DELIVERY:
            shipping.status = Shipping.Status.OUT_FOR_DELIVERY
        elif status == Shipping.Status.DELIVERED:
            shipping.status = Shipping.Status.DELIVERED
        shipping.save()

        return redirect('shipping:driver-shipping-list')

# @login_required
def update_shipping_status(request, pk):
    shipping = Shipping.objects.get(pk=pk)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status == Shipping.Status.DELIVERED:
            shipping.status = Shipping.Status.DELIVERED
        elif status == Shipping.Status.COMPLETE:
            shipping.status = Shipping.Status.COMPLETE
        shipping.save()

        return redirect('store:customer-order-list')
    
    return redirect('store:customer-order-list')
