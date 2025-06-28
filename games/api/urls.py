from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GameViewSet,
    GenreViewSet,
    DeveloperViewSet,
    PublisherViewSet,
)

# Criar um router e registrar os ViewSets
router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'developers', DeveloperViewSet, basename='developer')
router.register(r'publishers', PublisherViewSet, basename='publisher')

# As URLs da API são geradas automaticamente pelo router
urlpatterns = [
    path('', include(router.urls)),
]
