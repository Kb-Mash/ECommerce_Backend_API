from django.db import models
from seller.models import Seller


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
    #image = models.ImageField(upload_to='product_images/') install Pillow
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns:
            str: The name of the product.
        """
        return self.product_name
