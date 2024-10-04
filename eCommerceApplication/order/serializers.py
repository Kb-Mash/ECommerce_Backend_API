from rest_framework import serializers
from .models import Order, Cart, CartItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='cartitem_set', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'cart_price', 'items']
        read_only_fields = ['cart_price']

    def to_representation(self, instance):
        """
        Override to_representation to ensure cart_price is updated before serialization.
        """
        instance.update_cart_price()
        return super().to_representation(instance)

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, obj):
        """
        Returns the total price of the cart item.
        """
        return obj.get_total_price()
