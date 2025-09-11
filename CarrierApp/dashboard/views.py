from django.shortcuts import render
from django.http import JsonResponse
from order.models import Order
import json

def dashboard_view(request):
    """
    Renders the dashboard with stats and a list of all orders.
    """
    orders = Order.objects.all().order_by('-created_at')

    # Stats
    total_orders = orders.count()
    open_pos = orders.filter(status='open').count()
    unassigned = orders.filter(carrier__isnull=True).count() + orders.filter(carrier='').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'pending_shipments': open_pos,
        'unassigned': unassigned,
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
