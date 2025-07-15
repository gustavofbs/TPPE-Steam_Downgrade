from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Roteador dos endpoints do ViewSet
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),  # endpoints como /api/v1/users/
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # /api/v1/users/token/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # /api/v1/users/t
]