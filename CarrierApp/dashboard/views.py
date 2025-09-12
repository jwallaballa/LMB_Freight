from django.shortcuts import render
from django.http import JsonResponse
from order.models import Order
from carrier.models import Carrier
import json


def dashboard_view(request):
    """
    Renders the dashboard with stats and a list of all orders.
    """
    status_filter = request.GET.get('status', 'all')

    if status_filter == 'open':
        orders = Order.objects.filter(status='open').order_by('-created_at')
    elif status_filter == 'closed':
        orders = Order.objects.filter(status='closed').order_by('-created_at')
    else:
        orders = Order.objects.all().order_by('-created_at')

    carriers = Carrier.objects.all()

    # Stats
    total_orders = orders.count()  # Use the filtered queryset for the stats
    open_pos = orders.filter(status='open').count()
    unassigned = orders.filter(carrier__isnull=True).count() + orders.filter(carrier='').count()

    # Pie Chart Data
    open_orders_count = open_pos
    closed_orders_count = total_orders - open_pos

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'pending_shipments': open_pos,
        'unassigned': unassigned,
        'open_orders_count': open_orders_count,
        'closed_orders_count': closed_orders_count,
        'carriers': carriers,
    }
    return render(request, 'dashboard.html', context)


def update_order_view(request):
    """
    Receives an AJAX POST request to update a single field of an Order object.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('id')
            field_name = data.get('field')
            new_value = data.get('value')

            order = Order.objects.get(pk=order_id)
            setattr(order, field_name, new_value)
            order.save()
            return JsonResponse({'status': 'success'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)