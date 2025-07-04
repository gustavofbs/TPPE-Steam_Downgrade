from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FriendshipViewSet,
    GameReviewViewSet,
    ReviewCommentViewSet,
    UserActivityViewSet,
    GameRecommendationViewSet,
    UserGamePreferenceViewSet
)

# Criar um router e registrar os ViewSets
router = DefaultRouter()
router.register(r'friendships', FriendshipViewSet, basename='friendship')
router.register(r'reviews', GameReviewViewSet, basename='review')
router.register(r'comments', ReviewCommentViewSet, basename='comment')
router.register(r'activities', UserActivityViewSet, basename='activity')
router.register(r'recommendations', GameRecommendationViewSet, basename='recommendation')
router.register(r'preferences', UserGamePreferenceViewSet, basename='preference')

# As URLs da API são geradas automaticamente pelo router
urlpatterns = [
    path('', include(router.urls)),
]
