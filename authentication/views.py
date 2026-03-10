from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import login, logout
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import random

from .models import User, VerificationCode
from .serializers import RegisterSerializer, VerifyEmailSerializer, LoginSerializer, UserSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = serializer.save()
            code = str(random.randint(100000, 999999))
            VerificationCode.objects.create(
                user=user,
                code=code,
                expires_at=timezone.now() + timedelta(minutes=10)
            )
        return Response({'message':'Registered, verify your email', 'code':code}, status=status.HTTP_201_CREATED)

class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            #find the user
            user = User.objects.get(email=serializer.validated_data['email'])
            vc = VerificationCode.objects.filter(user=user, is_used=False).latest('expires_at')
            #todo
        except Exception:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        if not vc.is_valid() or vc.code != serializer.validated_data['code']:
            return Response({'error': 'Code is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            vc.is_used = True
            vc.save()
            user.is_email_verified = True
            user.save()

        return Response({'message': 'Email verified'})


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(User.serializer(user).data)

class LogoutView(APIView):
    def post (self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MeView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status = 401)
        return Response(UserSerializer(request.user).data)