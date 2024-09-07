from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from customer.serializers import CustomerSerializer
from seller.serializers import SellerSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegistrationView(APIView):
    def post(self, request):
        user_data = request.data.copy()
        user_serializer = CustomUserSerializer(data=user_data)
        
        if user_serializer.is_valid():
            user = user_serializer.save()

            if user.is_customer:
                customer_data = request.data.copy()
                customer_data['user'] = user.id
                customer_serializer = CustomerSerializer(data=customer_data)
                if customer_serializer.is_valid():
                    customer_serializer.save()
                    return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
                return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif user.is_seller:
                seller_data = request.data.copy()
                seller_data['user'] = user.id
                seller_serializer = SellerSerializer(data=seller_data)
                if seller_serializer.is_valid():
                    seller_serializer.save()
                    return Response(seller_serializer.data, status=status.HTTP_201_CREATED)
                return Response(seller_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"error": "Role must be specified."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        user_serializer = CustomUserSerializer(user)
        data = response.data
        data['message'] = 'You have logged in successfully.'
        data['user'] = user_serializer.data

        return Response(data, status=status.HTTP_200_OK)
