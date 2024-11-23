from django.contrib import admin
from .models import Booking, BookingHistory

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'booking_user', 'booking_parking_slot', 'booking_start_time', 'booking_end_time', 'booking_status', 'booking_payment_status', 'booking_total_cost')
    list_filter = ('booking_status', 'booking_payment_status')
    search_fields = ('booking_user__username', 'booking_parking_slot__name')
