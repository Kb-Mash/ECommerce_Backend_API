from rest_framework import serializers
from .models import CustomUser, Customer, Seller


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'is_customer', 'is_seller']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_customer=validated_data.get('is_customer', False),
            is_seller=validated_data.get('is_seller', False)
        )
        return user


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

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

    def create(self, validated_data):
        seller = Seller.objects.create(**validated_data)
        return seller
