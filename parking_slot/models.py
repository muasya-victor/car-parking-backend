from django.db import models


# Create your models here.
class ParkingSlot(models.Model):
    parking_slot_id = models.IntegerField(primary_key=True, unique=True)
    parking_slot_location = models.CharField(max_length=255)
    parking_slot_available = models.BooleanField(default=False)
    parking_slot_price_per_hour = models.FloatField(default=0)
    parking_slot_floor_number = models.IntegerField(default=0)
    parking_slot_capacity = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Parking Slot'
        verbose_name_plural = 'Parking Slots'