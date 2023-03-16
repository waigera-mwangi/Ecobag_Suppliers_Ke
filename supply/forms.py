from django import forms
from django.forms import ModelForm

from .models import *

class SupplyForm(ModelForm):
    class Meta:
        model = ProductSupply
        fields = '__all__'


class SupplyTenderForm(ModelForm):
    class Meta:
        model = SupplyTender
        fields = '__all__'