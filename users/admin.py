from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_first_name', 'user_last_name', 'user_role', 'user_is_active')
    search_fields = ('email', 'user_first_name', 'user_last_name')
    list_filter = ('user_role', 'is_staff', 'user_is_active')
    ordering = ('email',)


admin.site.unregister(Group)

