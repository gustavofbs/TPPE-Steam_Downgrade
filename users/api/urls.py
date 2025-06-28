from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Criar um router e registrar os ViewSets
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

# As URLs da API são geradas automaticamente pelo router
urlpatterns = [
    path('', include(router.urls)),
]
