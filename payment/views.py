from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payment.models import Payment
from payment.serializers import paymentSerializer
from users.models import CustomUser


# Create your views here.
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = paymentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'

    def get_queryset(self):
        user = self.request.user

        # if user.user_role == 'driver':
        #     return Payment.objects.filter(payment_user=self.request.user.user_id)
        #
        return Payment.objects.filter(payment_user=user.user_id)

    def perform_create(self, serializer):
        print(self.request.user, "user")
        serializer.save(payment_user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
