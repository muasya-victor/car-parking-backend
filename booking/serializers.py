from django.utils import timezone
from rest_framework import serializers
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from .models import Booking, BookingHistory

from rest_framework import serializers
from django.utils import timezone
from .models import Booking, CustomUser


class BookingSerializer(serializers.ModelSerializer):
    # booking_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='booking_user')

    class Meta:
        model = Booking
        fields = '__all__'
        # fields = [
        #     'booking_id',
        #     'booking_user',  # Displayed as `user_id` in the serializer
        #     'booking_start_time',
        #     'booking_end_time',
        #     'booking_status',
        #     'booking_payment_status',
        #     'booking_total_cost',
        # ]
        read_only_fields = ['booking_start_time', 'booking_total_cost']

    def validate(self, data):
        # Set booking_start_time to the current time
        data['booking_start_time'] = timezone.now()

        booking_end_time = data.get('booking_end_time')

        # Ensure the end time is provided and is after the start time
        if booking_end_time:
            # Calculate the duration in hours
            duration = booking_end_time - data['booking_start_time']
            if duration.total_seconds() <= 0:
                raise serializers.ValidationError("The end time must be after the current time.")

            duration_hours = duration.total_seconds() / 3600  # Convert duration to hours

            # Calculate and add booking_total_cost to validated data
            data['booking_total_cost'] = duration_hours * 100
        else:
            raise serializers.ValidationError("Booking end time must be provided.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['booking_user'] = request.user  

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Automatically assign the logged-in user to the booking_user field (if not already set)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['booking_user'] = request.user  # Use the logged-in user

        return super().update(instance, validated_data)

    # def create(self, validated_data):
    #     # Create the booking object and associate it with the user
    #     booking = Booking.objects.create(
    #         **validated_data
    #     )
    #     return booking
    #
    # def update(self, instance, validated_data):
    #     # You can implement custom logic if you want to update the booking details
    #     instance.booking_end_time = validated_data.get('booking_end_time', instance.booking_end_time)
    #     instance.booking_user = validated_data.get('booking_user', instance.booking_user)
    #     instance.save()
    #     return instance

class BookingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingHistory
        fields = '__all__'
