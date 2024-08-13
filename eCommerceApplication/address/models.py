from django.db import models
from customer.models import Customer


class Address(models.Model):
    """
    Represents an address associated with a customer.

    Attributes:
        street_number (CharField): The street number of the address.
        building_name (CharField): The name of the building (optional).
        address_line1 (CharField): The first line of the address.
        address_line2 (CharField): The second line of the address (optional).
        city (CharField): The city of the address.
        province (CharField): The province or state of the address.
        country (CharField): The country of the address.
        postal_code (CharField): The postal or ZIP code of the address.
        customer (ForeignKey): The customer associated with this address.
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
        """
        Returns:
            str: A formatted address string.
        """
        return f"{self.street_number} {self.address_line1}, {self.city}, {self.province}, {self.country}, {self.postal_code}"

