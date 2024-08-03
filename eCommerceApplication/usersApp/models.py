from django.db import models
from django.conf import settings


class Customer(models.Model):
    """
    Represents a customer in the system, linked to a user account.

    Attributes:
        user (OneToOneField): The user account associated with this customer.
        phone_number (CharField): The customer's phone number.
        created_at (DateTimeField): The timestamp when the customer record was created.
        payment_token (CharField): A token for payment information, used for integration with payment gateways.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        """
        Returns:
            str: The first name of the user.
        """
        return f'{self.user.first_name} {self.user.last_name} ({self.user.email})'
