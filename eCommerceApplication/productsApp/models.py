from django.db import models
from django.conf import settings


class Seller(models.Model):
    """
    Represents a seller in the system, linked to a user account.

    Attributes:
        user (OneToOneField): The user account associated with this seller.
        phone_number (CharField): The phone number of the seller.
        created_at (DateTimeField): The timestamp when the customer record was created. 
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the seller, including user details and phone number.

        Returns:
            str: A formatted string with seller details.
        """
        return f'{self.user.first_name} {self.user.last_name} {self.user.email} {self.phone_number}'


class Product(models.Model):
    """
    Represents a product in the system.

    Attributes:
        product_name (CharField): The name of the product.
        description (TextField): A description of the product.
        price (DecimalField): The price of the product.
        manufacturer (CharField): The manufacturer of the product.
        stock (IntegerField): The available stock of the product.
        category (CharField): The category of the product.
        image (ImageField): An image of the product.
        seller (ForeignKey): The seller associated with the product.
    """
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.CharField(max_length=255)
    stock = models.IntegerField()
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns:
            str: The name of the product.
        """
        return self.product_name

