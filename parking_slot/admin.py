from django.contrib import admin
from .models import ParkingSlot

@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = (
        'parking_slot_id',
        'parking_slot_location',
        'parking_slot_available',
        'parking_slot_price_per_hour',
        'parking_slot_floor_number',
        'parking_slot_capacity'
    )
    list_filter = ('parking_slot_available', 'parking_slot_floor_number')
    search_fields = ('parking_slot_location',)
    ordering = ('parking_slot_id',)

