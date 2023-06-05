from django import forms
from .models import Order, OrderItem
from accounts.models import User
from store.models import Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'is_completed']

    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    is_completed = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['county', 'town', 'phone_number']

    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    is_completed = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
