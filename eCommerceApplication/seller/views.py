from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Seller, Product
from .serializers import ProductSerializer
from authentication.models import CustomUser
from authentication.serializers import CustomUserSerializer
from .features_serializers import CurrentSellerSerializer, SellerUpdateSerializer, PasswordUpdateSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .utils import get_seller_instance
from .utils import success_response, error_response, not_found_response, no_content_response


### Seller Views ###

# Get logged in seller
class CurrentSellerView(RetrieveAPIView):
    serializer_class = CurrentSellerSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance, err_response = get_seller_instance(self.request)

        if err_response:
            return err_response

        serializer = self.get_serializer(instance)
        return success_response("Seller data retrieved successfully", data=serializer.data)

# Upadate logged in seller
class SellerUpdateView(UpdateAPIView):
    serializer_class = SellerUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance, err_response = get_seller_instance(self.request)

        if err_response:
            return err_response

        # PATCH request for partial updates
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return success_response("Seller updated successfully", data=serializer.data)

        return error_response("Invalid data provided", errors=serializer.errors)

# Delete logged in seller
class SellerDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance, err_response = get_seller_instance(self.request)

        if err_response:
            return err_response

        # To-Do: implement soft deletion
        self.perform_destroy(instance)
        return no_content_response("Seller deleted successfully")

# Update password for logged in seller
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

### Product Views ###

# Create Product
class ProductCreateView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        seller, err_response = get_seller_instance(self.request)

        if err_response:
            return err_response

        data = request.data.copy()

        serializer = self.get_serializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save(seller=seller)
            return success_response("Product created successfully", data=serializer.data)

        return error_response("Invalid data provided", errors=serializer.errors)

# Get current seller's product
class ProductRetrieveView(RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        seller, _ = get_seller_instance(self.request)
        return Product.objects.filter(seller=seller)

    def get_object(self):
        try:
            return super().get_object()
        except Product.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        if product is None:
            return not_found_response("Product does not exist")

        serializer = self.get_serializer(product)
        return success_response("Product retrieved successfully", data=serializer.data)

# Update current seller's product
class ProductUpdateView(UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        seller, _ = get_seller_instance(self.request)
        return Product.objects.filter(seller=seller)

    def get_object(self):
        try:
            return super().get_object()
        except Product.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        if product is None:
            return not_found_response("Product does not exist")

        seller, err_response = get_seller_instance(self.request)

        if err_response:
            return err_response

        data = request.data.copy()
        data['seller'] = seller.id

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(product, data=data, context={'request': request}, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return success_response("Product updated successfully", data=serializer.data)

        return error_response("Invalid data provided", errors=serializer.errors)

# Delete current seller's product
class ProductDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        seller, _ = get_seller_instance(self.request)
        return Product.objects.filter(seller=seller)

    def get_object(self):
        try:
            return super().get_object()
        except Product.DoesNotExist:
            return None

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product is None:
            return not_found_response("Product does not exist")

        self.perform_destroy(address)

        return no_content_response("Product deleted successfully")
