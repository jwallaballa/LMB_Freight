import pytest
from django.urls import reverse
from order.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_add_order_view_get_request(client):
    """
    Test that the add_order_view returns a 200 status code for a GET request.
    The 'client' fixture is provided by pytest-django.
    """
    # Changed 'add_order_view' to 'add_order' to match the URL name in urls.py
    url = reverse('add_order')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_order_view_post_request_valid_data(client):
    """
    Test that a POST request with valid data successfully creates an Order object
    and redirects to the dashboard.
    """
    # Changed 'add_order_view' to 'add_order' to match the URL name in urls.py
    url = reverse('add_order')
    data = {
        'product_name': 'Test Product',
        'quantity': 10,
        'price': 100.00
    }
    response = client.post(url, data)
    assert response.status_code == 302 # Assumes a redirect on success
    assert Order.objects.count() == 1
    # Check that the redirect URL is correct, assuming a dashboard URL exists
    # If your dashboard URL name is different, you will need to update this line
    assert response.url == reverse('dashboard')
