from rest_framework import serializers
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from .models import Booking, BookingHistory


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'booking_user',
            'booking_start_time',
            'booking_end_time',
            'booking_status',
            'booking_payment_status',
            'booking_total_cost',
        ]
        read_only_fields = ['booking_total_cost']  # Ensure it's not editable by the user

    def validate(self, data):
        booking_start_time = data.get('booking_start_time')
        booking_end_time = data.get('booking_end_time')

        # Ensure both start and end times are provided
        if booking_start_time and booking_end_time:
            # Calculate the duration in hours
            duration = booking_end_time - booking_start_time
            duration_hours = duration.total_seconds() / 3600  # Convert duration to hours

            # Calculate and add booking_total_cost to validated data
            data['booking_total_cost'] = duration_hours * 100
        else:
            raise serializers.ValidationError("Both booking start time and end time must be provided.")

        return data

    def create(self, validated_data):
        booking_user = validated_data.get('booking_user')
        booking_start_time = validated_data.get('booking_start_time')
        booking_end_time = validated_data.get('booking_end_time')
        booking_total_cost = validated_data.get('booking_total_cost')

        # Create the booking object and associate it with the user
        booking = Booking.objects.create(
            booking_user=booking_user,
            booking_end_time=booking_end_time,
            booking_start_time=booking_start_time,
            booking_total_cost=booking_total_cost,
            **validated_data
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
