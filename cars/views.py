from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import CarMake, CarModel, PartCategory, Part, Vehicle, VehiclePhoto
from .serializers import (
    CarMakeSerializer, CarModelSerializer, PartCategorySerializer,
    PartListSerializer, PartDetailSerializer, VehicleSerializer, 
    VehicleCreateSerializer, VehiclePhotoSerializer
)


class CarMakeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CarMake.objects.all()
    serializer_class = CarMakeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'name_ar']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def models(self, request, pk=None):
        """Get all models for a specific make"""
        make = self.get_object()
        models = make.models.filter(is_active=True)
        serializer = CarModelSerializer(models, many=True)
        return Response(serializer.data)


class CarModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CarModel.objects.select_related('make').all()
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['make', 'is_active', 'body_type', 'year_start']
    search_fields = ['name', 'name_ar', 'make__name', 'make__name_ar']
    ordering_fields = ['name', 'year_start', 'created_at']
    ordering = ['make__name', 'name']
    
    @action(detail=True, methods=['get'])
    def compatible_parts(self, request, pk=None):
        """Get all compatible parts for a specific model"""
        model = self.get_object()
        parts = model.compatible_parts.filter(is_active=True)
        serializer = PartListSerializer(parts, many=True)
        return Response(serializer.data)


class PartCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = PartCategory.objects.filter(parent=None)  # Only root categories by default
    serializer_class = PartCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'name_ar']
    ordering_fields = ['sort_order', 'name']
    ordering = ['sort_order', 'name']
    
    @action(detail=False, methods=['get'])
    def all(self, request):
        """Get all categories including subcategories"""
        categories = PartCategory.objects.filter(is_active=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def parts(self, request, pk=None):
        """Get all parts in a category"""
        category = self.get_object()
        parts = category.parts.filter(is_active=True)
        serializer = PartListSerializer(parts, many=True)
        return Response(serializer.data)


class PartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Part.objects.select_related('category').prefetch_related('compatible_models').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_universal', 'is_active']
    search_fields = ['name', 'name_ar', 'part_number', 'description']
    ordering_fields = ['name', 'part_number', 'created_at']
    ordering = ['category__sort_order', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PartDetailSerializer
        return PartListSerializer
    
    @action(detail=False, methods=['get'])
    def search_by_vehicle(self, request):
        """Search parts compatible with specific vehicle"""
        make_id = request.query_params.get('make')
        model_id = request.query_params.get('model')
        year = request.query_params.get('year')
        
        queryset = self.get_queryset().filter(is_active=True)
        
        if model_id:
            queryset = queryset.filter(compatible_models__id=model_id)
        elif make_id:
            queryset = queryset.filter(compatible_models__make_id=make_id)
        
        if year:
            queryset = queryset.filter(
                compatible_models__year_start__lte=year
            ).filter(
                models.Q(compatible_models__year_end__gte=year) | 
                models.Q(compatible_models__year_end__isnull=True)
            )
        
        serializer = self.get_serializer(queryset.distinct(), many=True)
        return Response(serializer.data)


class VehicleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Vehicle.objects.select_related('make', 'model', 'received_by').prefetch_related('photos').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['make', 'model', 'year', 'condition', 'is_dismantled']
    search_fields = ['vin', 'make__name', 'model__name', 'color']
    ordering_fields = ['intake_date', 'year', 'created_at']
    ordering = ['-intake_date']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VehicleCreateSerializer
        return VehicleSerializer
    
    @action(detail=True, methods=['post'])
    def dismantle(self, request, pk=None):
        """Mark vehicle as dismantled"""
        from django.utils import timezone
        vehicle = self.get_object()
        vehicle.is_dismantled = True
        vehicle.dismantled_date = timezone.now()
        vehicle.save()
        serializer = self.get_serializer(vehicle)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def extracted_parts(self, request, pk=None):
        """Get all parts extracted from this vehicle"""
        from inventory.serializers import InventoryItemListSerializer
        vehicle = self.get_object()
        parts = vehicle.extracted_parts.all()
        serializer = InventoryItemListSerializer(parts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_photo(self, request, pk=None):
        """Upload a photo for the vehicle"""
        vehicle = self.get_object()
        serializer = VehiclePhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vehicle=vehicle)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
