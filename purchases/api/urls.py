from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CartViewSet,
    OrderViewSet,
    LibraryViewSet,
    DownloadHistoryViewSet,
    WishlistViewSet,
    CouponViewSet
)

# Criar um router e registrar os ViewSets
router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'library', LibraryViewSet, basename='library')
router.register(r'downloads', DownloadHistoryViewSet, basename='downloadhistory')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'coupons', CouponViewSet, basename='coupon')

# As URLs da API são geradas automaticamente pelo router
urlpatterns = [
    path('', include(router.urls)),
]
