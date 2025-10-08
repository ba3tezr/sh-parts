from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import WarehouseLocation, InventoryItem, InventoryItemImage, StockMovement


@admin.register(WarehouseLocation)
class WarehouseLocationAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'aisle', 'shelf', 'bin', 'is_active')
    list_filter = ('warehouse', 'is_active')
    search_fields = ('warehouse', 'aisle', 'shelf', 'bin', 'description')
    ordering = ('warehouse', 'aisle', 'shelf', 'bin')


class InventoryItemImageInline(admin.TabularInline):
    model = InventoryItemImage
    extra = 1


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('sku', 'part', 'condition', 'status', 'quantity', 'selling_price', 
                   'location', 'is_low_stock', 'added_at')
    list_filter = ('condition', 'status', 'added_at')
    search_fields = ('sku', 'part__name', 'barcode')
    readonly_fields = ('sku', 'qr_code', 'added_at', 'updated_at')
    inlines = [InventoryItemImageInline]
    
    fieldsets = (
        (_('Item Information'), {
            'fields': ('sku', 'part', 'vehicle_source', 'condition', 'status')
        }),
        (_('Quantity'), {
            'fields': ('quantity', 'min_quantity')
        }),
        (_('Location & Tracking'), {
            'fields': ('location', 'barcode', 'qr_code')
        }),
        (_('Pricing'), {
            'fields': ('cost_price', 'selling_price')
        }),
        (_('Additional'), {
            'fields': ('notes', 'added_by')
        }),
        (_('Timestamps'), {
            'fields': ('added_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = _('Low Stock')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('item', 'movement_type', 'quantity', 'from_location', 'to_location', 
                   'performed_by', 'performed_at')
    list_filter = ('movement_type', 'performed_at')
    search_fields = ('item__sku', 'reference', 'reason')
    date_hierarchy = 'performed_at'
    readonly_fields = ('performed_at',)
