from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name',
            'po_number',
            'ship_date',
            'order_number',
            'location_from',
            'carrier',  # changed from location_to
            'cost',
            # 'status'  # include this only if you want it editable in the form
        ]
        widgets = {
            "ship_date": forms.DateInput(attrs={'type': 'date'}),
        }
