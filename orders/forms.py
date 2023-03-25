from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'is_completed']

    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    is_completed = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
