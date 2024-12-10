from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Booking, BookingHistory
from .serializers import BookingSerializer, BookingHistorySerializer
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO


class BookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Booking instances.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Restrict the queryset so that only admins see all bookings,
        while regular users only see their own bookings.
        """
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(booking_user=user)


class BookingHistoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing BookingHistory instances.
    """
    queryset = BookingHistory.objects.all()
    serializer_class = BookingHistorySerializer
    permission_classes = [AllowAny]  # Allow access without login


from django.utils.timezone import now
from django.db.models import Prefetch
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from parking_slot.models import ParkingSlot
from booking.models import Booking


class PDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Fetch all bookings with related parking slot and user details
        bookings = Booking.objects.select_related('booking_user', 'booking_parking_slot')

        context = {
            'current_date': now().strftime('%Y-%m-%d %H:%M:%S'),
            'bookings': bookings,
        }

        # Render the template
        html_string = render_to_string('booking_report.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=all_bookings_report.pdf'

        # Generate PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
        if not pdf.err:
            response.write(result.getvalue())
            return response
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
