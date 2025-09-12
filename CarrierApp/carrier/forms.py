from django import forms
from django.forms import inlineformset_factory
from .models import Carrier, Rate

class CarrierForm(forms.ModelForm):
    class Meta:
        model = Carrier
        fields = ['name', 'contact_name', 'email', 'phone','location']

RateFormSet = inlineformset_factory(
    Carrier,
    Rate,
    fields=('rate', 'description'),
    extra=1,
    can_delete=True
)
