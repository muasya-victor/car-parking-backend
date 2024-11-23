from django.db import models

from booking.models import Booking
from parking_slot.models import ParkingSlot
from users.models import CustomUser


# Create your models here.
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True,editable=False)
    payment_date = models.DateField(auto_now_add=True)
    payment_amount = models.FloatField(default=0)
    payment_parking_slot = models.ForeignKey(ParkingSlot, related_name='payments', on_delete=models.CASCADE, null=True, blank=True)
    payment_booking = models.ForeignKey(Booking, related_name='payments', on_delete=models.CASCADE, null=True, blank=True)
    payment_complete = models.BooleanField(default=False)
    payment_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'