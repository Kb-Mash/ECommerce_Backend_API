from django.conf import settings
from django.db import models


class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - Seller'


class Product(models.Model):
    """
    Represents a product in the system.
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
        return self.product_name
