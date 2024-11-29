from rest_framework.routers import DefaultRouter
from .views import ParkingSlotViewSet,PDFView
from django.urls import path, include


router = DefaultRouter()
router.register(r'parking-slots', ParkingSlotViewSet, basename='parking_slots')

urlpatterns = [
    path('', include(router.urls)),
    path('slot/report/', PDFView.as_view(), name='slot-report-pdf')
]
