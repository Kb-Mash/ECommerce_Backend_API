from rest_framework import serializers
from .models import Customer, Address
from user.serializers import CustomUserSerializer
from django.contrib.auth import update_session_auth_hash


class CurrentCustomerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['user', 'id', 'phone_number', 'created_at', 'payment_token']

class CustomerUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=False)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = Customer
        fields = ['email', 'phone_number']

    def update(self, instance, validated_data):
        # Handle update to User model's email
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')
        
        if email:
            # Access and update the email directly on the user instance
            instance.user.email = email
            instance.user.save()

        # Handle updates to the Customer model
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()

        return instance

class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def save(self):
        user = self.context['request'].user
        #old_password = self.validated_data['old_password']
        new_password = self.validated_data['new_password']
        
        user.set_password(new_password)
        user.save()
        
        # Keep the user logged in after password change
        update_session_auth_hash(self.context['request'], user)
