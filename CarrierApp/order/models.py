from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    customer_name = models.CharField(max_length=100)
    po_number = models.CharField(max_length=50)
    ship_date = models.DateField(null=True, blank=True)
    order_number = models.CharField(max_length=50, null=True, blank=True)
    location_from = models.CharField(max_length=200, null=True, blank=True)
    carrier = models.CharField(max_length=200, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number or self.po_number} for {self.customer_name}"
