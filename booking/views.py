from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Booking, BookingHistory
from .serializers import BookingSerializer, BookingHistorySerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Booking instances.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]


class BookingHistoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing BookingHistory instances.
    """
    queryset = BookingHistory.objects.all()
    serializer_class = BookingHistorySerializer
    permission_classes = [AllowAny]  # Allow access without login
