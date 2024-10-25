from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import serializers
from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom claims
        token['email'] = user.email
        token['user_role'] = user.user_role
        return token

    def validate(self, attrs):
        user_email = attrs.get('email')
        user_password = attrs.get('password')

        user = CustomUser.objects.filter(email=user_email).first()
        if user and user.check_password(user_password):
            return super().validate(attrs)
        else:
            raise serializers.ValidationError("Invalid credentials")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
