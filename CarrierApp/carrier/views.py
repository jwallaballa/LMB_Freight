from django.shortcuts import render, get_object_or_404, redirect
from .models import Carrier
from .forms import CarrierForm

def carrier_list(request):
    carriers = Carrier.objects.all()
    return render(request, 'carrier/carrier_list.html', {'carriers': carriers})

def carrier_detail(request, pk):
    carrier = get_object_or_404(Carrier, pk=pk)
    return render(request, 'carrier/carrier_detail.html', {'carrier': carrier})

def add_carrier(request):
    if request.method == 'POST':
        form = CarrierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('carrier_list')
    else:
        form = CarrierForm()
    return render(request, 'carrier/carrier_form.html', {'form': form})
