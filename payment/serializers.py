from rest_framework import serializers

from payment.models import Payment


class paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        payment_user = validated_data.get('payment_user')
        payment_amount = validated_data.get('payment_amount')
        payment_parking_slot = validated_data.get('payment_parking_slot')

        payment = Payment.objects.create(
            payment_amount=payment_amount,
            payment_user=payment_user,
            payment_parking_slot=payment_parking_slot,
        )

        return payment

