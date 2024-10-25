from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'user_first_name', 'user_last_name', 'user_role', 'user_country_code', 'user_is_active', 'password']
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
