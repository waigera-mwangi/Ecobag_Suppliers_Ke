from django import forms
from .models import LoanApplication, LoanRepayment, Savings


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['amount', 'due_date', 'limit', 'purpose', 'status']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount'
            }),
            'due_date': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'due-date'
            }),
            'limit': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'limit'
            }),
            'purpose': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'purpose'
            }),
            'status': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'status'
            }),

        }
