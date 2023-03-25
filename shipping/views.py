from django.shortcuts import render
from .models import UserPickUpStation
from .forms import UserPickUpStationForm
from accounts.models import User
from django.urls import reverse_lazy
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