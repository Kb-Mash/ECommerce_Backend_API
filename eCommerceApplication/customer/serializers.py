from rest_framework import serializers
from .models import Customer, Address


class CustomerSerializer(serializers.ModelSerializer):
    # user = CustomUserSerializer() remove nested serializer for view-handled user creation

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        #user_data = validated_data.pop('user') remove nested user creation logic
        #user = CustomUserSerializer.create(CustomUserSerializer(), validated_data=user_data)
        customer = Customer.objects.create(**validated_data)
        return customer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
