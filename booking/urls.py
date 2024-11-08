from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, BookingHistoryViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'booking-history', BookingHistoryViewSet)

urlpatterns = router.urls
