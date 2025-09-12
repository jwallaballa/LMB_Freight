from django.db import models

class Carrier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Rate(models.Model):
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name='rates')
    rate = models.FloatField()
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.carrier.name} - ${self.rate}"