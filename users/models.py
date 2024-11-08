import uuid

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_role', 'admin')  # Ensure role is set for superuser

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('driver', 'Driver'),
    ]

    COUNTRY_CODES = [
        ('+254', 'Kenya'),
        ('+255', 'Tanzania'),
    ]

    user_id = models.IntegerField(unique=True, editable=False, verbose_name="user_id",primary_key=True)
    email = models.EmailField(unique=True, verbose_name="user_email")
    user_first_name = models.CharField(max_length=255, verbose_name="user_first_name")
    user_last_name = models.CharField(max_length=255, verbose_name="user_last_name")
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="user_role")
    user_country_code = models.CharField(max_length=20, choices=COUNTRY_CODES, default='+254',
                                         verbose_name="user_country_code", blank=True, null=True)
    user_phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="user_phone_number")
    user_is_active = models.BooleanField(default=True, verbose_name="user_is_active")
    is_staff = models.BooleanField(default=False, verbose_name="user_is_staff")
    is_superuser = models.BooleanField(default=False, verbose_name="user_is_superuser")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="user_created_at")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_role']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs):
        self.user_is_active = False
        self.save(update_fields=['user_is_active'])

        

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"