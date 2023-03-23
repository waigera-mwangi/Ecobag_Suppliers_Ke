from django.forms import ModelForm
from django import forms
from .models import *

class DeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'

        widgets = {
            'order': forms.Select(attrs={
                'class': 'form-control', 'id': 'order'
            }),
            'courier_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'courier_name'
            }),
        }