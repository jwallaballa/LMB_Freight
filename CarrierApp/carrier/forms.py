from django import forms
from .models import Carrier

class CarrierForm(forms.ModelForm):
    class Meta:
        model = Carrier
        fields = ['name', 'contact_name', 'email', 'phone',]
