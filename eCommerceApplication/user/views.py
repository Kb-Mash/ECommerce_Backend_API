from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import CustomUserSerializer, CustomerSerializer, SellerSerializer
# from rest_framework_simplejwt.tokens import RefreshToken - To-Do


class UserRegistrationView(APIView):
    def post(self, request):
        user_data = request.data.copy()
        user_serializer = CustomUserSerializer(data=user_data)
        
        if user_serializer.is_valid():
            user = user_serializer.save()

            if user.is_customer:
                customer_data = {'user': user.id, **request.data}
                customer_serializer = CustomerSerializer(data=customer_data)
                if customer_serializer.is_valid():
                    customer_serializer.save()
                    return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
                return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif user.is_seller:
                seller_data = {'user': user.id, **request.data}
                seller_serializer = SellerSerializer(data=seller_data)
                if seller_serializer.is_valid():
                    seller_serializer.save()
                    return Response(seller_serializer.data, status=status.HTTP_201_CREATED)
                return Response(seller_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"error": "Role must be specified."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            serializer = CustomUserSerializer(user)

            # Return the tokens and user data
            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
"""
