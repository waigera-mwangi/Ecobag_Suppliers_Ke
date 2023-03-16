from django import forms
from django.forms import ModelForm

from .models import *

class OrderForm(ModelForm):
    class Meta:
        # model = Order
        fields = '__all__'


class DeliveryForm(forms.ModelForm):
    class Meta:
        # model = Delivery
        fields = '__all__'

        widgets = {
            'order': forms.Select(attrs={
                'class': 'form-control', 'id': 'order'
            }),
            'courier_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'courier_name'
            }),
        }

from django.forms import ModelForm

from store.models import Product


class OrderItemForm(ModelForm):
    class Meta:
        # model = OrderItem
        fields = ['product', 'quantity']


class OrderPaymentForm(ModelForm):
    class Meta:
        # model = OrderPayment
        fields = ['mpesa', 'phone', 'amount']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'