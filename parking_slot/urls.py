from rest_framework.routers import DefaultRouter
from .views import ParkingSlotViewSet

router = DefaultRouter()
router.register(r'parking-slots', ParkingSlotViewSet, basename='parking_slots')

urlpatterns = router.urls
