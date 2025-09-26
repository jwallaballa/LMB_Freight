from django.shortcuts import render
from django.http import JsonResponse
from order.models import Order
from carrier.models import Carrier
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from calendar import month_abbr
import datetime
import json


def dashboard_view(request):
    """
    Renders the dashboard with stats and a list of all orders.
    """
    status_filter = request.GET.get('status', 'all')
    current_year = datetime.date.today().year

    if status_filter == 'open':
        orders = Order.objects.filter(status='open').order_by('-created_at')
    elif status_filter == 'closed':
        orders = Order.objects.filter(status='closed').order_by('-created_at')
    else:
        orders = Order.objects.all().order_by('-created_at')

    all_carriers = Carrier.objects.all()

    # Stats
    total_orders = orders.count()
    open_pos = orders.filter(status='open').count()
    unassigned = orders.filter(carrier__isnull=True).count() + orders.filter(carrier='').count()

    # Pie Chart Data
    open_orders_count = open_pos
    closed_orders_count = total_orders - open_pos

    # Monthly orders for the bar chart
    orders_by_month = Order.objects.filter(
        created_at__year=current_year
    ).annotate(
        month=ExtractMonth('created_at')
    ).values(
        'month'
    ).annotate(
        count=Count('id')
    ).order_by(
        'month'
    )

    # Separate queries for open and closed orders
    open_orders_by_month = Order.objects.filter(
        created_at__year=current_year,
        status='open'
    ).annotate(
        month=ExtractMonth('created_at')
    ).values(
        'month'
    ).annotate(
        count=Count('id')
    ).order_by(
        'month'
    )

    closed_orders_by_month = Order.objects.filter(
        created_at__year=current_year,
        status='closed'
    ).annotate(
        month=ExtractMonth('created_at')
    ).values(
        'month'
    ).annotate(
        count=Count('id')
    ).order_by(
        'month'
    )

    # Prepare data for Chart.js, ensuring all 12 months are included
    orders_dict = {item['month']: item['count'] for item in orders_by_month}
    open_orders_dict = {item['month']: item['count'] for item in open_orders_by_month}
    closed_orders_dict = {item['month']: item['count'] for item in closed_orders_by_month}

    months_labels = [month_abbr[i] for i in range(1, 13)]
    orders_counts = [orders_dict.get(i, 0) for i in range(1, 13)]
    open_orders_counts = [open_orders_dict.get(i, 0) for i in range(1, 13)]
    closed_orders_counts = [closed_orders_dict.get(i, 0) for i in range(1, 13)]

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'pending_shipments': open_pos,
        'unassigned': unassigned,
        'open_orders_count': open_orders_count,
        'closed_orders_count': closed_orders_count,
        'all_carriers': all_carriers,
        'orders_counts_json': json.dumps(orders_counts),
        'months_labels_json': json.dumps(months_labels),
        'open_orders_counts_json': json.dumps(open_orders_counts),
        'closed_orders_counts_json': json.dumps(closed_orders_counts),
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