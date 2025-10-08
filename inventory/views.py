from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import WarehouseLocation, InventoryItem, InventoryItemImage, StockMovement
from .serializers import (
    WarehouseLocationSerializer, InventoryItemListSerializer, 
    InventoryItemDetailSerializer, InventoryItemCreateSerializer,
    InventoryItemImageSerializer, StockMovementSerializer
)


class WarehouseLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = WarehouseLocation.objects.all()
    serializer_class = WarehouseLocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['warehouse', 'is_active']
    search_fields = ['warehouse', 'aisle', 'shelf', 'bin']
    ordering_fields = ['warehouse', 'aisle', 'shelf', 'bin']
    ordering = ['warehouse', 'aisle', 'shelf', 'bin']


class InventoryItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = InventoryItem.objects.select_related(
        'part', 'vehicle_source', 'location', 'added_by'
    ).prefetch_related('images').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['part', 'part__category', 'condition', 'status', 'location']
    search_fields = ['sku', 'part__name', 'part__name_ar', 'part__part_number', 'barcode']
    ordering_fields = ['sku', 'selling_price', 'quantity', 'added_at']
    ordering = ['-added_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InventoryItemDetailSerializer
        elif self.action == 'create':
            return InventoryItemCreateSerializer
        return InventoryItemListSerializer
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get items with low stock"""
        items = self.get_queryset().filter(
            quantity__lte=models.F('min_quantity')
        ).filter(status='AVAILABLE')
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available items"""
        items = self.get_queryset().filter(status='AVAILABLE', quantity__gt=0)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def adjust_quantity(self, request, pk=None):
        """Adjust item quantity"""
        item = self.get_object()
        quantity = request.data.get('quantity', 0)
        reason = request.data.get('reason', '')
        
        old_quantity = item.quantity
        item.quantity = quantity
        item.save()
        
        # Create stock movement record
        StockMovement.objects.create(
            item=item,
            movement_type='ADJUSTMENT',
            quantity=quantity - old_quantity,
            reason=reason,
            performed_by=request.user
        )
        
        serializer = self.get_serializer(item)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        """Upload an image for the inventory item"""
        item = self.get_object()
        serializer = InventoryItemImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(item=item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = StockMovement.objects.select_related(
        'item', 'from_location', 'to_location', 'performed_by'
    ).all()
    serializer_class = StockMovementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item', 'movement_type', 'performed_by']
    search_fields = ['item__sku', 'reason', 'reference']
    ordering_fields = ['performed_at']
    ordering = ['-performed_at']
