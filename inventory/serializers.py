from rest_framework import serializers
from .models import WarehouseLocation, InventoryItem, InventoryItemImage, StockMovement
from cars.serializers import PartListSerializer, VehicleSerializer


class WarehouseLocationSerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()
    full_location = serializers.SerializerMethodField()
    
    class Meta:
        model = WarehouseLocation
        fields = ['id', 'warehouse', 'aisle', 'shelf', 'bin', 'description', 
                 'is_active', 'items_count', 'full_location']
    
    def get_items_count(self, obj):
        return obj.items.filter(status='AVAILABLE').count()
    
    def get_full_location(self, obj):
        return str(obj)


class InventoryItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItemImage
        fields = ['id', 'image', 'caption', 'is_primary', 'uploaded_at']


class InventoryItemListSerializer(serializers.ModelSerializer):
    part_name = serializers.CharField(source='part.name', read_only=True)
    part_name_ar = serializers.CharField(source='part.name_ar', read_only=True)
    location_name = serializers.CharField(source='location.__str__', read_only=True)
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = InventoryItem
        fields = ['id', 'sku', 'part', 'part_name', 'part_name_ar', 'condition',
                 'condition_display', 'status', 'status_display', 'quantity', 'min_quantity',
                 'location', 'location_name', 'cost_price', 'selling_price', 'qr_code',
                 'is_low_stock', 'added_at']


class InventoryItemDetailSerializer(serializers.ModelSerializer):
    part_details = PartListSerializer(source='part', read_only=True)
    vehicle_source_details = VehicleSerializer(source='vehicle_source', read_only=True)
    location_details = WarehouseLocationSerializer(source='location', read_only=True)
    added_by_name = serializers.CharField(source='added_by.get_full_name', read_only=True)
    images = InventoryItemImageSerializer(many=True, read_only=True)
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = InventoryItem
        fields = ['id', 'sku', 'part', 'part_details', 'vehicle_source', 'vehicle_source_details',
                 'condition', 'condition_display', 'status', 'status_display', 'quantity', 'min_quantity',
                 'location', 'location_details', 'cost_price', 'selling_price', 'barcode', 'qr_code',
                 'notes', 'added_by', 'added_by_name', 'images', 'is_low_stock', 'added_at', 'updated_at']


class InventoryItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['part', 'vehicle_source', 'condition', 'status', 'quantity', 'min_quantity',
                 'location', 'cost_price', 'selling_price', 'barcode', 'notes', 'added_by']


class StockMovementSerializer(serializers.ModelSerializer):
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    item_part_name = serializers.CharField(source='item.part.name', read_only=True)
    from_location_name = serializers.CharField(source='from_location.__str__', read_only=True)
    to_location_name = serializers.CharField(source='to_location.__str__', read_only=True)
    performed_by_name = serializers.CharField(source='performed_by.get_full_name', read_only=True)
    movement_type_display = serializers.CharField(source='get_movement_type_display', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = ['id', 'item', 'item_sku', 'item_part_name', 'movement_type', 'movement_type_display',
                 'quantity', 'from_location', 'from_location_name', 'to_location', 'to_location_name',
                 'reason', 'reference', 'performed_by', 'performed_by_name', 'performed_at']
