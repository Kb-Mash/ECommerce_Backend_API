from rest_framework import serializers
from .models import Seller, Product


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

    def create(self, validated_data):
        seller = Seller.objects.create(**validated_data)
        return seller


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['seller']
