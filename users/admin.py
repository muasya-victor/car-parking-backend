import random
import string
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'user_first_name',
        'user_last_name',
        'get_user_email',
        'user_last_login',
        'user_role',
        'user_is_superuser',
        'password',  # Add the password field to the list display
    )
    search_fields = ('email', 'user_first_name', 'user_last_name')
    list_filter = ('user_role', 'is_staff', 'user_is_active')
    ordering = ('email',)

    def get_user_email(self, obj):
        return obj.email
    get_user_email.short_description = _('user email')  # Lowercase here

    def user_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    user_groups.short_description = _('user groups')  # Lowercase here

    def user_last_login(self, obj):
        return obj.last_login
    user_last_login.short_description = _('user last login')  # Lowercase here

    def user_is_active(self, obj):
        return obj.user_is_active
    user_is_active.short_description = _('user is active')  # Lowercase here

    def user_is_superuser(self, obj):
        return obj.is_superuser
    user_is_superuser.short_description = _('user is superuser')  # Lowercase here

    # Custom method to display a masked password
    def password(self, obj):
        # Generate a random string of 12 characters
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    password.short_description = _('user password')  # Lowercase here

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

# Unregister the default Group model
admin.site.unregister(Group)
