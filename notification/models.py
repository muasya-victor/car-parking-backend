from django.db import models

from users.models import CustomUser


# Create your models here.
class Notification(models.Model):
    NOTIFICATION_CHOICES = [
        ('Booking', 'booking'),
        ('Payment', 'payment'),
        ('Alert', 'alert')
    ]
    NOTIFICATION_STATUS_CHOICES = [
        ('Booking', 'booking'),
        ('Payment', 'payment'),
        ('Alert', 'alert')
    ]
    notification_id = models.AutoField(primary_key=True, editable=False)
    notification_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_CHOICES)
    notification_message = models.TextField()
    notification_date = models.DateTimeField(auto_now_add=True)
    notification_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'