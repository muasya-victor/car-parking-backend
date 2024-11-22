from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'notification_id',
            'notification_user',
            'notification_type',
            'notification_message',
            'notification_date',
            'notification_read',
        ]
        read_only_fields = ['notification_id', 'notification_date']
