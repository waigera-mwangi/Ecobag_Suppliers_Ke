from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['transaction_id']
        widgets = {
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
