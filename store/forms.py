from django import forms
from django.forms import ModelForm

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            # 'sortno': forms.NumberInput(attrs={
            #     'class': 'form-control', 'id': 'sortno'
            # }),
            'image': forms.FileInput(attrs={
                'class': 'form-control', 'id': 'image'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'price'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'quantity'
            }),
        }


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


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'description', 'quantity']



class OrderItemForm(ModelForm):
    class Meta:
        # model = OrderItem
        fields = ['product', 'quantity']


class OrderPaymentForm(ModelForm):
    class Meta:
        # model = OrderPayment
        fields = ['mpesa', 'phone', 'amount']