from django.contrib import admin
from .models import Booking,BookingHistory


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking_id',
        'booking_user',
        'booking_start_time',
        'booking_end_time',
        'booking_status',
        'booking_payment_status',
        'booking_total_cost'
    )
    list_filter = ('booking_status', 'booking_payment_status')
    search_fields = ('booking_user__email',)  # Assuming CustomUser has an 'email' field
    ordering = ('booking_start_time',)


# @admin.register(BookingHistory)
# class BookingHistoryAdmin(admin.ModelAdmin):
#     list_display = ('booking_history_id', 'get_booking_user', 'get_booking_start_time', 'get_booking_end_time')
#     list_filter = ('booking_history_booking__booking_user',)
#     search_fields = ('booking_history_id', 'booking_history_booking__booking_user__user_email')
#     readonly_fields = ('booking_history_id',)

    def get_booking_user(self, obj):
        return obj.booking_history_booking.booking_user.email

    def get_booking_start_time(self, obj):
        return obj.booking_history_booking.booking_start_time

    def get_booking_end_time(self, obj):
        return obj.booking_history_booking.booking_end_time

    get_booking_user.short_description = 'Booking History User'
    get_booking_start_time.short_description = 'Booking History Start Time'
    get_booking_end_time.short_description = 'Booking History End Time'
