from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarMakeViewSet, CarModelViewSet, PartCategoryViewSet, PartViewSet, VehicleViewSet

app_name = 'cars'

router = DefaultRouter()
router.register(r'makes', CarMakeViewSet, basename='make')
router.register(r'models', CarModelViewSet, basename='model')
router.register(r'categories', PartCategoryViewSet, basename='category')
router.register(r'parts', PartViewSet, basename='part')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')

urlpatterns = [
    path('', include(router.urls)),
]
