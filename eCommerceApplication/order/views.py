from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializer, CartItemSerializer
from .models import Cart, CartItem
from seller.models import Product
from .utils import get_customer_instance
from .utils import success_response, error_response, not_found_response, no_content_response

# Retrieve Cart (GET)
class CartDetailView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        customer, err_response = get_customer_instance(self.request)
        if err_response:
            return err_response

        try:
            cart = customer.cart
        except Cart.DoesNotExist:
            return not_found_response("Cart not found")

        serializer = self.get_serializer(cart)
        return success_response("Cart data retrieved successfully", data=serializer.data)

# Add Item to Cart (POST)
class CartItemCreateView(CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        customer, err_response = get_customer_instance(self.request)
        if err_response:
            return err_response

        # Ensure the customer has a cart, or create one
        cart, created = Cart.objects.get_or_create(customer=customer)

        data = request.data.copy()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return not_found_response("Product not found")

        data['cart'] = cart.id
        data['product'] = product.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            cart.update_cart_price()  # Update cart total price
            return success_response("Item added to cart successfully", data=serializer.data)

        return error_response("Invalid data provided", errors=serializer.errors)

# Remove specific item from cart (DELETE)
class CartItemDeleteView(DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer, _ = get_customer_instance(self.request)
        return CartItem.objects.filter(cart__customer=customer)

    def get_object(self):
        try:
            return super().get_object()
        except CartItem.DoesNotExist:
            return None

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        if item is None:
            return not_found_response("Cart item does not exist")

        cart = item.cart
        self.perform_destroy(item)
        cart.update_cart_price()  # Update cart total price after removal

        return no_content_response("Cart item removed successfully")

# Clear entire cart (DELETE)
class CartClearView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer, _ = get_customer_instance(self.request)
        return CartItem.objects.filter(cart__customer=customer)

    def destroy(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        if not cart_items.exists():
            return no_content_response("Cart is already empty")

        cart_items.delete()

        # Optionally reset the cart price
        customer, _ = get_customer_instance(self.request)
        cart = customer.cart
        cart.cart_price = 0
        cart.save()

        return no_content_response("Cart cleared successfully")

