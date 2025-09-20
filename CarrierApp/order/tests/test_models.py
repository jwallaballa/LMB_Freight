import pytest
from order.models import Order

@pytest.mark.django_db
def test_order_creation():
    """
    Test that an Order object can be created successfully.
    """
    order = Order.objects.create(
        customer_name='John Doe',
        po_number='PO-12345',
        order_number='ORD-98765'
    )
    assert order.customer_name == 'John Doe'
    assert order.po_number == 'PO-12345'
    assert order.status == 'open'
    assert Order.objects.count() == 1

@pytest.mark.django_db
def test_order_str_representation():
    """
    Test the __str__ method of the Order model.
    """
    order = Order.objects.create(
        customer_name='Jane Smith',
        order_number='ORD-001'
    )
    assert str(order) == "Order ORD-001 for Jane Smith"