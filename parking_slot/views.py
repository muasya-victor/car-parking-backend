from io import BytesIO

from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import viewsets
from xhtml2pdf import pisa

from parking_slot.models import ParkingSlot
from parking_slot.serializers import ParkingSlotSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, permissions, status

from users.models import CustomUser


class ParkingSlotViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ParkingSlot instances.
    """
    serializer_class = ParkingSlotSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Filter the queryset to return only available parking slots
        return ParkingSlot.objects.filter(parking_slot_available=True)


class PDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        slots = ParkingSlot.objects.all()

        serializer = ParkingSlotSerializer(
            slots, many=True, context={'request': request})
        context = {'slots': serializer.data}

        html_string = render_to_string('slot_report.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=slot_report.pdf'

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
        if not pdf.err:
            response.write(result.getvalue())
            return response
        return HttpResponse('We had some errors <pre>' + html_string +'</pre>')
