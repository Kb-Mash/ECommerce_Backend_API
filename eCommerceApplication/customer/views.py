from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Address
from .serializers import AddressSerializer
from authentication.models import CustomUser
from authentication.serializers import CustomUserSerializer
from .features_serializers import CurrentCustomerSerializer, CustomerUpdateSerializer, PasswordUpdateSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .utils import get_customer_instance
from .utils import success_response, error_response, not_found_response, no_content_response


### Customer Views ###

# Get logged in customer
class CurrentCustomerView(RetrieveAPIView):
    serializer_class = CurrentCustomerSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance, err_response = get_customer_instance(self.request)

        if err_response:
            return err_response

        serializer = self.get_serializer(instance)
        return success_response("Customer data retrieved successfully", data=serializer.data)

# Upadate logged in customer
class CustomerUpdateView(UpdateAPIView):
    serializer_class = CustomerUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance, err_response = get_customer_instance(self.request)

        if err_response:
            return err_response

        # PATCH request for partial updates
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return success_response("Customer updated successfully", data=serializer.data)

        return error_response("Invalid data provided", errors=serializer.errors)

# Delete logged in customer
class CustomerDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance, err_response = get_customer_instance(self.request)

        if err_response:
            return err_response

        # To-Do: implement soft deletion
        self.perform_destroy(instance)
        return no_content_response("Customer deleted successfully")

# Update password for logged in customer
class PasswordUpdateView(UpdateAPIView):
    serializer_class = PasswordUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']  # Use PATCH method

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return success_response("Password updated successfully", data=serializer.data)

        return error_response("Invalid data provided", errors=serializer.errors)

### Address Views ###

# Create Address
class AddressCreateView(CreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        customer, err_response = get_customer_instance(self.request)

        if err_response:
            return err_response

        data = request.data.copy()

        serializer = self.get_serializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save(customer=customer)
            return success_response("Address created successfully", data=serializer.data)

        return error_response("Invalid data provided", errors=serializer.errors)

# Get current customer's address
class AddressRetrieveView(RetrieveAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer, _ = get_customer_instance(self.request)
        return Address.objects.filter(customer=customer)

    def get_object(self):
        try:
            return super().get_object()
        except Address.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        address = self.get_object()
        if address is None:
            return not_found_response("Address does not exist")

        serializer = self.get_serializer(address)
        return success_response("Address retrieved successfully", data=serializer.data)

class AddressUpdateView(UpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer, _ = get_customer_instance(self.request)
        return Address.objects.filter(customer=customer)

    def get_object(self):
        try:
            return super().get_object()
        except Address.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        address = self.get_object()
        if address is None:
            return not_found_response("Address does not exist")

        customer, err_response = get_customer_instance(self.request)

        if err_response:
            return err_response

        data = request.data.copy()
        data['customer'] = customer.id

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(address, data=data, context={'request': request}, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return success_response("Address updated successfully", data=serializer.data)

        return error_response("Invalid data provided", errors=serializer.errors)

# Delete current customer's address
class AddressDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer, _ = get_customer_instance(self.request)
        return Address.objects.filter(customer=customer)

    def get_object(self):
        try:
            return super().get_object()
        except Address.DoesNotExist:
            return None

    def destroy(self, request, *args, **kwargs):
        address = self.get_object()
        if address is None:
            return not_found_response("Address does not exist")

        self.perform_destroy(address)

        return no_content_response("Address deleted successfully")
