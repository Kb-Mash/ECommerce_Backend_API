from rest_framework import serializers
from .models import Seller

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

    def create(self, validated_data):
        seller = Seller.objects.create(**validated_data)
        return seller
