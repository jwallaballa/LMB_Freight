from django.shortcuts import render, get_object_or_404, redirect
from .models import Carrier, Rate
from .forms import CarrierForm, RateFormSet
from order.models import Order
from django.http import JsonResponse
from .models import Rate
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json



def carrier_list(request):
    carriers = Carrier.objects.all()
    all_carriers = Carrier.objects.all()

    return render(request, 'carrier/carrier_list.html', {
        'carriers': carriers,
        'all_carriers': all_carriers
    })

def carrier_detail(request, pk):
    carrier = get_object_or_404(Carrier, pk=pk)
    open_orders = Order.objects.filter(carrier=carrier, status='open').order_by('-created_at')


    from .forms import RateFormSet
    formset = RateFormSet(instance=carrier)

    all_carriers = Carrier.objects.all()

    context = {
        'carrier': carrier,
        'open_orders': open_orders,
        'formset': formset,
        'all_carriers': all_carriers,
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


    all_carriers = Carrier.objects.all()

    return render(request, 'carrier/carrier_form.html', {
        'form': form,
        'formset': formset,
        'all_carriers': all_carriers
    })


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


    all_carriers = Carrier.objects.all()

    return render(request, 'carrier/carrier_form.html', {
        'form': form,
        'formset': formset,
        'all_carriers': all_carriers
    })


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




@require_POST
def delete_rate(request, pk):
    try:
        rate = get_object_or_404(Rate, pk=pk)
        rate.delete()
        return JsonResponse({'status': 'success', 'message': 'Rate deleted successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@require_POST
@csrf_exempt
def save_rate(request):
    try:
        data = json.loads(request.body)
        rate_id = data.get('id')
        carrier_id = data.get('carrier_id')
        rate_value = data.get('rate')
        description_value = data.get('description')

        if not carrier_id:
            return JsonResponse({'status': 'error', 'message': 'Carrier ID is required.'}, status=400)

        carrier = get_object_or_404(Carrier, pk=carrier_id)

        # Check if rate_id exists. If so, update the existing rate.
        if rate_id:
            rate = get_object_or_404(Rate, pk=rate_id)
            if rate_value is not None:
                rate.rate = float(rate_value) if rate_value else None
            rate.description = description_value
            rate.save()
        else:
            # If rate_id doesn't exist, create a new rate.
            rate = Rate.objects.create(
                carrier=carrier,
                rate=float(rate_value) if rate_value else None,
                description=description_value
            )

        return JsonResponse({'status': 'success', 'rate_id': rate.id})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid data format for rate or description.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
