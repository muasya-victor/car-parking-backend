from django.utils import timezone
from datetime import timedelta

from django.db import models

from payment.models import Payment
from users.models import CustomUser


# Create your models here.
class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True, unique=True, editable=False)
    booking_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, help_text="Driver Booking The Slot")
    booking_start_time = models.DateTimeField(default=timezone.now)
    booking_end_time = models.DateTimeField()
    booking_status = models.CharField(max_length=50, choices=(
        ('Confirmed', 'confirmed'),
        ('Canceled', 'canceled'),
        ('Completed', 'completed'),
        ), default="Confirmed")
    booking_payment_status = models.CharField(max_length=50, choices=(
        ('Paid', 'paid'),
        ('Unpaid', 'unpaid'),
        ), default='Unpaid')
    booking_total_cost = models.FloatField(editable=False)

    def save(self, *args, **kwargs):
        # Calculate the duration in hours
        duration = self.booking_end_time - self.booking_start_time
        duration_hours = duration.total_seconds() / 3600  # Convert duration to hours
        self.booking_total_cost = duration_hours * 100  # Calculate the total cost

        # Call the superclass save method
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'


class BookingHistory(models.Model):
    booking_history_id = models.IntegerField(primary_key=True, unique=True, editable=False)
    booking_history_booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Booking History'
        verbose_name_plural = 'Booking Histories'