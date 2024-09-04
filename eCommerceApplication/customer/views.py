from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Address
from .serializers import AddressSerializer
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from .features_serializers import CurrentCustomerSerializer, CustomerUpdateSerializer, PasswordUpdateSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView


### Customer Views ###

# Get logged in customer
class CurrentCustomerView(RetrieveAPIView):
    serializer_class = CurrentCustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Customer.objects.get(user=self.request.user)

# Upadate logged in customer
class CustomerUpdateView(UpdateAPIView):
    serializer_class = CustomerUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Customer.objects.get(user=self.request.user)

# Delete logged in customer
class CustomerDeleteView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Customer.objects.get(user=self.request.user)

# Update password for logged in customer
class PasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### Address Views ###

# Create Address
class AddressCreateView(CreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        customer = Customer.objects.get(user=self.request.user)
        serializer.save(customer=customer)

# Get current customer's address
class AddressRetrieveView(RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return Address.objects.filter(customer=customer)

# Update current customer's address
class AddressUpdateView(UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return Address.objects.filter(customer=customer)

# Delete current customer's address
class AddressDeleteView(DestroyAPIView):
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return Address.objects.filter(customer=customer)
