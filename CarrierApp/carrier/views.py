from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Carrier, Rate
from .forms import CarrierForm, RateFormSet
from order.models import Order
import json


def carrier_list(request):
    carriers = Carrier.objects.all()
    return render(request, 'carrier/carrier_list.html', {'carriers': carriers})


def carrier_detail(request, pk):
    carrier = get_object_or_404(Carrier, pk=pk)

    # Fetch all open orders where the carrier name matches the current carrier
    open_orders = Order.objects.filter(carrier__iexact=carrier.name, status='open')

    context = {
        'carrier': carrier,
        'open_orders': open_orders,
    }
    return render(request, 'carrier/carrier_detail.html', context)


def add_carrier(request):
    if request.method == 'POST':
        form = CarrierForm(request.POST)
        formset = RateFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            carrier = form.save()
            formset.instance = carrier
            formset.save()
            return redirect('carrier_list')
    else:
        form = CarrierForm()
        formset = RateFormSet()
    return render(request, 'carrier/carrier_form.html', {'form': form, 'formset': formset})


def edit_carrier(request, pk):
    carrier = get_object_or_404(Carrier, pk=pk)
    if request.method == 'POST':
        form = CarrierForm(request.POST, instance=carrier)
        formset = RateFormSet(request.POST, instance=carrier)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('carrier_list')
    else:
        form = CarrierForm(instance=carrier)
        formset = RateFormSet(instance=carrier)
    return render(request, 'carrier/carrier_form.html', {'form': form, 'formset': formset})


def update_carrier_field(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            field_name = data.get('field')
            new_value = data.get('value')

            carrier = Carrier.objects.get(pk=pk)
            setattr(carrier, field_name, new_value)
            carrier.save()
            return JsonResponse({'status': 'success'})
        except Carrier.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Carrier not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def update_carrier_rate(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            field_name = data.get('field')
            new_value = data.get('value')

            rate = Rate.objects.get(pk=pk)
            # Handle rate field value conversion
            if field_name == 'rate':
                new_value = float(new_value.replace('$', ''))

            setattr(rate, field_name, new_value)
            rate.save()
            return JsonResponse({'status': 'success'})
        except Rate.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Rate not found.'}, status=404)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid rate value.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)