from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import ParkingSlot
from .serializers import ParkingSlotSerializer


class ParkingSlotViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ParkingSlot instances.
    """
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer
    permission_classes = [AllowAny]  # Allow access without login
