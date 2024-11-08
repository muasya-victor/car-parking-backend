from rest_framework import serializers
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from .models import Booking, BookingHistory


class BookingSerializer(serializers.ModelSerializer):
    booking_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)
    user = CustomUserSerializer(source='booking_user', read_only=True)

    class Meta:
        model = Booking
        fields = ['booking_id', 'booking_start_time', 'booking_user', 'booking_total_cost',
                  'booking_end_time', 'booking_status', 'user', 'booking_user']

    def create(self, validated_data):
        booking_user = validated_data.get('booking_user')
        booking_end_time = validated_data.get('booking_end_time')

        # Create the booking object and associate it with the user
        booking = Booking.objects.create(
            booking_user=booking_user,
            booking_end_time=booking_end_time,
        )
        return booking

    def update(self, instance, validated_data):
        # You can implement custom logic if you want to update the booking details
        instance.booking_end_time = validated_data.get('booking_end_time', instance.booking_end_time)
        instance.booking_user = validated_data.get('booking_user', instance.booking_user)
        instance.save()
        return instance
class BookingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingHistory
        fields = '__all__'
