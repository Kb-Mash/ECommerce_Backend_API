from django.conf import settings
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user.email} - Customer'


class Address(models.Model):
    """
    Represents an address associated with a customer.
    """

    street_number = models.CharField(max_length=20)
    building_name = models.CharField(max_length=255, blank=True, null=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.street_number} {self.address_line1}, {self.city}, {self.province}, {self.country}, {self.postal_code}"

