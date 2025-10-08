from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WarehouseLocationViewSet, InventoryItemViewSet, StockMovementViewSet

app_name = 'inventory'

router = DefaultRouter()
router.register(r'locations', WarehouseLocationViewSet, basename='location')
router.register(r'items', InventoryItemViewSet, basename='item')
router.register(r'movements', StockMovementViewSet, basename='movement')

urlpatterns = [
    path('', include(router.urls)),
]
