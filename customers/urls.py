from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, CustomerCreditViewSet, CustomerNoteViewSet

app_name = 'customers'

router = DefaultRouter()
router.register(r'', CustomerViewSet, basename='customer')
router.register(r'credits', CustomerCreditViewSet, basename='credit')
router.register(r'notes', CustomerNoteViewSet, basename='note')

urlpatterns = [
    path('', include(router.urls)),
]
