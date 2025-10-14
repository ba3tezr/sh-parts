from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.utils import timezone
from .models import WarehouseLocation, InventoryItem, InventoryItemImage, StockMovement, LocationTransfer
from .serializers import (
    WarehouseLocationSerializer, InventoryItemListSerializer,
    InventoryItemDetailSerializer, InventoryItemCreateSerializer,
    InventoryItemImageSerializer, StockMovementSerializer, LocationTransferSerializer
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

    @action(detail=True, methods=['post'])
    def upload_images(self, request, pk=None):
        """Upload images for an inventory item"""
        item = self.get_object()
        images = request.FILES.getlist('images')
        caption = request.data.get('caption', '')
        is_primary = request.data.get('is_primary', 'false').lower() == 'true'

        if not images:
            return Response(
                {'detail': 'No images provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If this is primary, unset other primary images
        if is_primary:
            InventoryItemImage.objects.filter(item=item, is_primary=True).update(is_primary=False)

        uploaded_images = []
        for image in images:
            img = InventoryItemImage.objects.create(
                item=item,
                image=image,
                caption=caption,
                is_primary=is_primary and len(uploaded_images) == 0  # Only first image is primary
            )
            uploaded_images.append(img)

        from .serializers import InventoryItemImageSerializer
        serializer = InventoryItemImageSerializer(uploaded_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def set_primary_image(self, request, pk=None):
        """Set an image as primary"""
        item = self.get_object()
        image_id = request.data.get('image_id')

        if not image_id:
            return Response(
                {'detail': 'image_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Unset all primary images
            InventoryItemImage.objects.filter(item=item).update(is_primary=False)

            # Set new primary
            image = InventoryItemImage.objects.get(id=image_id, item=item)
            image.is_primary = True
            image.save()

            return Response({'detail': 'Primary image updated successfully'})
        except InventoryItemImage.DoesNotExist:
            return Response(
                {'detail': 'Image not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
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


class LocationTransferViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = LocationTransfer.objects.select_related(
        'item', 'item__part', 'from_location', 'to_location',
        'requested_by', 'approved_by', 'completed_by'
    ).all()
    serializer_class = LocationTransferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item', 'status', 'from_location', 'to_location']
    search_fields = ['item__sku', 'reason']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a transfer request"""
        transfer = self.get_object()

        if transfer.status != 'PENDING':
            return Response(
                {'detail': 'Only pending transfers can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )

        transfer.status = 'APPROVED'
        transfer.approved_by = request.user
        transfer.approved_at = timezone.now()
        transfer.save()

        serializer = self.get_serializer(transfer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a transfer (actually move the item)"""
        transfer = self.get_object()

        if transfer.status not in ['PENDING', 'APPROVED']:
            return Response(
                {'detail': 'Only pending or approved transfers can be completed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if item has enough quantity
        if transfer.item.quantity < transfer.quantity:
            return Response(
                {'detail': 'Insufficient quantity in source location'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create stock movement
        movement = StockMovement.objects.create(
            item=transfer.item,
            movement_type='TRANSFER',
            quantity=transfer.quantity,
            from_location=transfer.from_location,
            to_location=transfer.to_location,
            reason=f"Transfer #{transfer.id}: {transfer.reason}",
            reference=f"TRANSFER-{transfer.id}",
            performed_by=request.user
        )

        # Update item location
        transfer.item.location = transfer.to_location
        transfer.item.save()

        # Update transfer status
        transfer.status = 'COMPLETED'
        transfer.completed_by = request.user
        transfer.completed_at = timezone.now()
        transfer.stock_movement = movement
        transfer.save()

        serializer = self.get_serializer(transfer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a transfer request"""
        transfer = self.get_object()

        if transfer.status == 'COMPLETED':
            return Response(
                {'detail': 'Completed transfers cannot be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )

        transfer.status = 'CANCELLED'
        transfer.save()

        serializer = self.get_serializer(transfer)
        return Response(serializer.data)
