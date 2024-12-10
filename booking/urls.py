from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, BookingHistoryViewSet, PDFView
from django.urls import path, include


router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'booking-history', BookingHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('booking/report/', PDFView.as_view(), name='slot-report-pdf')
]