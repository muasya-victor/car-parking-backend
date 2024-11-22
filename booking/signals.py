from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from notification.models import Notification  # Assuming the Notification model is in the 'notification' app


@receiver(post_save, sender=Booking)
def create_booking_notification(sender, instance, created, **kwargs):
    if created:  # Only trigger for new bookings
        Notification.objects.create(
            notification_user=instance.booking_user,
            notification_type='Booking',
            notification_message=f"A new booking has been created with ID {instance.booking_id}.",
        )
