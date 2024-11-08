from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser
from rest_framework.exceptions import ValidationError


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['user_role'] = user.user_role
        return token

    def validate(self, attrs):
        user_email = attrs.get('email')
        user_password = attrs.get('password')

        # Check if the user exists and the password is correct
        user = CustomUser.objects.filter(email=user_email).first()
        if user and user.check_password(user_password):
            # Generate token and include additional user data
            data = super().validate(attrs)
            data['user'] = {
                'email': user.email,
                'user_role': user.user_role,
                'user_first_name': user.user_first_name,
                'user_last_name': user.user_last_name
            }
            return data
        else:
            raise ValidationError("Invalid credentials")


class MiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_first_name', 'user_last_name']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'user_first_name', 'user_last_name', 'user_role', 'user_country_code', 'user_is_active', 'password', 'user_id', 'user_phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            user_first_name=validated_data['user_first_name'],
            user_last_name=validated_data['user_last_name'],
            user_role=validated_data['user_role'],
            user_country_code=validated_data['user_country_code'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
