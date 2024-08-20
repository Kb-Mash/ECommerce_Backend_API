from rest_framework import serializers
from django.contrib.auth.models import User
from authentication.serializers import UserSerializer
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
