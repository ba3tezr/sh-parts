from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from cars.models import Part, Vehicle
import qrcode
from io import BytesIO
from django.core.files import File


class WarehouseLocation(models.Model):
    warehouse = models.CharField(_('warehouse'), max_length=100)
    aisle = models.CharField(_('aisle'), max_length=20, blank=True)
    shelf = models.CharField(_('shelf'), max_length=20, blank=True)
    bin = models.CharField(_('bin'), max_length=20, blank=True)
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('warehouse location')
        verbose_name_plural = _('warehouse locations')
        ordering = ['warehouse', 'aisle', 'shelf', 'bin']
        unique_together = ['warehouse', 'aisle', 'shelf', 'bin']

    def __str__(self):
        parts = [self.warehouse]
        if self.aisle:
            parts.append(f"Aisle {self.aisle}")
        if self.shelf:
            parts.append(f"Shelf {self.shelf}")
        if self.bin:
            parts.append(f"Bin {self.bin}")
        return " - ".join(parts)


class InventoryItem(models.Model):
    CONDITION_CHOICES = [
        ('NEW', _('New')),
        ('USED_EXCELLENT', _('Used - Excellent')),
        ('USED_GOOD', _('Used - Good')),
        ('USED_FAIR', _('Used - Fair')),
        ('REFURBISHED', _('Refurbished')),
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', _('Available')),
        ('RESERVED', _('Reserved')),
        ('SOLD', _('Sold')),
        ('DAMAGED', _('Damaged')),
        ('RETURNED', _('Returned')),
    ]

    sku = models.CharField(_('SKU'), max_length=50, unique=True, editable=False)
    part = models.ForeignKey(Part, on_delete=models.PROTECT, related_name='inventory_items', 
                            verbose_name=_('part'))
    vehicle_source = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='extracted_parts', verbose_name=_('source vehicle'))
    
    condition = models.CharField(_('condition'), max_length=20, choices=CONDITION_CHOICES)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    
    quantity = models.IntegerField(_('quantity'), default=1)
    min_quantity = models.IntegerField(_('minimum quantity'), default=1)
    
    location = models.ForeignKey(WarehouseLocation, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='items', verbose_name=_('location'))
    
    cost_price = models.DecimalField(_('cost price'), max_digits=10, decimal_places=2, 
                                    null=True, blank=True)
    selling_price = models.DecimalField(_('selling price'), max_digits=10, decimal_places=2)
    
    barcode = models.CharField(_('barcode'), max_length=100, blank=True)
    qr_code = models.ImageField(_('QR code'), upload_to='qr_codes/', blank=True, null=True)
    
    notes = models.TextField(_('notes'), blank=True)
    
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                related_name='added_items', verbose_name=_('added by'))
    added_at = models.DateTimeField(_('added at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('inventory item')
        verbose_name_plural = _('inventory items')
        ordering = ['-added_at']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['status']),
            models.Index(fields=['part', 'condition']),
        ]

    def __str__(self):
        return f"{self.sku} - {self.part.name}"

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self.generate_sku()
        
        if not self.qr_code:
            self.generate_qr_code()
        
        super().save(*args, **kwargs)

    def generate_sku(self):
        import random
        import string
        from django.utils import timezone
        
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"SKU-{timestamp}-{random_str}"

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_data = f"SKU:{self.sku}"
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        file_name = f'qr_{self.sku}.png'
        self.qr_code.save(file_name, File(buffer), save=False)
        buffer.close()

    @property
    def is_low_stock(self):
        return self.quantity <= self.min_quantity


class InventoryItemImage(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, 
                            related_name='images', verbose_name=_('item'))
    image = models.ImageField(_('image'), upload_to='inventory_items/')
    caption = models.CharField(_('caption'), max_length=200, blank=True)
    is_primary = models.BooleanField(_('primary image'), default=False)
    uploaded_at = models.DateTimeField(_('uploaded at'), auto_now_add=True)

    class Meta:
        verbose_name = _('inventory item image')
        verbose_name_plural = _('inventory item images')
        ordering = ['-is_primary', '-uploaded_at']

    def __str__(self):
        return f"Image for {self.item.sku}"


class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('IN', _('Stock In')),
        ('OUT', _('Stock Out')),
        ('ADJUSTMENT', _('Adjustment')),
        ('TRANSFER', _('Transfer')),
        ('RETURN', _('Return')),
    ]

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, 
                            related_name='movements', verbose_name=_('item'))
    movement_type = models.CharField(_('movement type'), max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField(_('quantity'))
    from_location = models.ForeignKey(WarehouseLocation, on_delete=models.SET_NULL, 
                                     null=True, blank=True, related_name='movements_from',
                                     verbose_name=_('from location'))
    to_location = models.ForeignKey(WarehouseLocation, on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='movements_to',
                                   verbose_name=_('to location'))
    
    reason = models.TextField(_('reason'), blank=True)
    reference = models.CharField(_('reference'), max_length=100, blank=True)
    
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                    related_name='stock_movements', verbose_name=_('performed by'))
    performed_at = models.DateTimeField(_('performed at'), auto_now_add=True)

    class Meta:
        verbose_name = _('stock movement')
        verbose_name_plural = _('stock movements')
        ordering = ['-performed_at']

    def __str__(self):
        return f"{self.movement_type} - {self.item.sku} - {self.quantity} units"
