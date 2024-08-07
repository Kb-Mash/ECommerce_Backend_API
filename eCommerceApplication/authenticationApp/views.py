from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from sessionsApp.models import UserSession
import uuid


@api_view(['POST'])
@csrf_exempt
def register(request):
    # Handle registration logic
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)
    if user is not None:
        login(request, user)
        session_key = str(uuid.uuid4())
        UserSession.objects.create(user=user, session_key=session_key)
        return Response({'message': 'Login successful'})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view['POST'])
@csrf_exempt
def logout_view(request):
    session_key = request.data.get('session_key') # Extract session key from request body
    if session_key:
        UserSession.objects.filter(session_key=session_key).delete()
    logout(request)
    return Response({'message': 'Logout successful'})
