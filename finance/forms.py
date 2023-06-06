from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['transaction_id']
        widgets = {
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['county','town','phone_number']
        widgets = {
            'county': forms.TextInput(attrs={'class': 'form-control'}),
            'town': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            
        }


