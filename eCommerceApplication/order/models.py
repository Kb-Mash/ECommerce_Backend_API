from django.db import models
from customer.models import Customer
from seller.models import Product


class Order(models.Model):
    """
    Represents an order placed by a customer.

    Attributes:
        status (CharField): The status of the order (e.g., pending, completed).
        created_at (DateTimeField): The timestamp when the order was created.
        total_price (DecimalField): The total price of the order.
        customer (ForeignKey): The customer who placed the order.
    """
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns:
            str: The status and total price of the order.
        """
        return f'Order {self.id} - Status: {self.status}, Total Price: {self.total_price}'


class Cart(models.Model):
    """
    Represents a shopping cart associated with a customer.

    Attributes:
        customer (OneToOneField): The customer who owns the cart.
        cart_price (DecimalField): The total price of the cart.
    """
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    cart_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_cart_price(self):
        """
        Updates the cart_price by calculating the sum of all cart item prices.
        """
        
        """
        total_price = 0
        for item in self.cartitem_set.all():
            total_price += item.product.price * item.quantity
        """
        total_price = sum(item.get_total_price() for item in self.cartitem_set.all())
        self.cart_price = total_price
        self.save()

    def __str__(self):
        """
        Returns:
            str: The ID of the cart associated with the customer.
        """
        return f'Cart for {self.customer.email}'


class CartItem(models.Model):
    """
    Represents an item in the shopping cart.

    Attributes:
        quantity (IntegerField): The quantity of the product in the cart.
        product (ForeignKey): The product added to the cart.
        cart (ForeignKey): The cart that contains the item.
    """
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def get_total_price(self):
        """
        Calculates the total price of this cart item (product price * quantity).
        """
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        """
        Overrides the save method to update the cart's total price whenever a cart item is added or modified.
        """
        super().save(*args, **kwargs)
        self.cart.update_cart_price()

    def delete(self, *args, **kwargs):
    """
    Overrides the delete method to update the cart's total price when a cart item is removed.
    """
        super().delete(*args, **kwargs)
        self.cart.update_cart_price()

    def __str__(self):
        """
        Returns:
            str: The product and quantity of the cart item.
        """
        return f'{self.product.name} - Quantity: {self.quantity}'
