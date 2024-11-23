from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from parking_slot.models import ParkingSlot
from parking_slot.serializers import ParkingSlotSerializer


class ParkingSlotViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ParkingSlot instances.
    """
    serializer_class = ParkingSlotSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Filter the queryset to return only available parking slots
        return ParkingSlot.objects.filter(parking_slot_available=True)
