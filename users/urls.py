from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, CustomTokenObtainPairView, CurrentUserViewSet, PDFView,UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'users/active', CurrentUserViewSet, basename='current_user')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('report/', PDFView.as_view(), name='user-list-pdf')
]
