from django.forms import ModelForm
from .models import Brand
from django import forms

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['order_tno', 'brand_name', 'brand_logo']

        widgets = {
            'order_tno': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_logo': forms.FileInput(attrs={'class': 'form-control-file'})
        }
        
        labels = {
            'order_tno': 'Transaction ID'
        }
