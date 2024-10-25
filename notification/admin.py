from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'notification_user', 'notification_type', 'notification_date', 'notification_read')
    list_filter = ('notification_type', 'notification_read', 'notification_date')
    search_fields = ('notification_user__email', 'notification_message')
    ordering = ('-notification_date',)
    readonly_fields = ('notification_date',)


admin.site.register(Notification, NotificationAdmin)
