from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from customers.models import Customer
from inventory.models import InventoryItem
from decimal import Decimal


class Sale(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', _('Draft')),
        ('CONFIRMED', _('Confirmed')),
        ('COMPLETED', _('Completed')),
        ('CANCELLED', _('Cancelled')),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', _('Unpaid')),
        ('PARTIAL', _('Partially Paid')),
        ('PAID', _('Fully Paid')),
    ]

    invoice_number = models.CharField(_('invoice number'), max_length=50, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, 
                                related_name='sales', verbose_name=_('customer'))
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    payment_status = models.CharField(_('payment status'), max_length=20, 
                                     choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(_('paid amount'), max_digits=10, decimal_places=2, default=0)
    
    notes = models.TextField(_('notes'), blank=True)
    
    sales_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                    related_name='sales', verbose_name=_('sales person'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)

    class Meta:
        verbose_name = _('sale')
        verbose_name_plural = _('sales')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.invoice_number} - {self.customer.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        
        self.calculate_totals()
        self.update_payment_status()
        
        super().save(*args, **kwargs)

    def generate_invoice_number(self):
        from django.utils import timezone
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        return f"INV-{timestamp}"

    def calculate_totals(self):
        # If the Sale is not saved yet, related items manager can't be used
        if not self.pk:
            # Keep current totals (likely zero) until items are added
            self.subtotal = self.subtotal or 0
            self.total_amount = (self.subtotal - self.discount_amount + self.tax_amount)
            return
        items = self.items.all()
        self.subtotal = sum(item.total_price for item in items)
        self.total_amount = self.subtotal - self.discount_amount + self.tax_amount

    def update_payment_status(self):
        if self.paid_amount >= self.total_amount:
            self.payment_status = 'PAID'
        elif self.paid_amount > 0:
            self.payment_status = 'PARTIAL'
        else:
            self.payment_status = 'UNPAID'

    @property
    def balance_due(self):
        return self.total_amount - self.paid_amount


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, 
                            related_name='items', verbose_name=_('sale'))
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT, 
                                      related_name='sale_items', verbose_name=_('inventory item'))
    
    quantity = models.IntegerField(_('quantity'), default=1)
    unit_price = models.DecimalField(_('unit price'), max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(_('discount %'), max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(_('total price'), max_digits=10, decimal_places=2)
    
    notes = models.TextField(_('notes'), blank=True)

    class Meta:
        verbose_name = _('sale item')
        verbose_name_plural = _('sale items')
        ordering = ['id']

    def __str__(self):
        return f"{self.inventory_item.part.name} x{self.quantity}"

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.inventory_item.selling_price
        
        if self.discount_percent > 0:
            self.discount_amount = (self.unit_price * self.quantity * self.discount_percent) / 100
        
        self.total_price = (self.unit_price * self.quantity) - self.discount_amount
        
        super().save(*args, **kwargs)


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CASH', _('Cash')),
        ('CARD', _('Credit/Debit Card')),
        ('BANK_TRANSFER', _('Bank Transfer')),
        ('CHEQUE', _('Cheque')),
        ('CREDIT', _('Store Credit')),
    ]

    payment_number = models.CharField(_('payment number'), max_length=50, unique=True, editable=False)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, 
                            related_name='payments', verbose_name=_('sale'))
    
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    payment_method = models.CharField(_('payment method'), max_length=20, choices=PAYMENT_METHOD_CHOICES)
    
    reference_number = models.CharField(_('reference number'), max_length=100, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                   related_name='received_payments', verbose_name=_('received by'))
    payment_date = models.DateTimeField(_('payment date'), auto_now_add=True)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.payment_number} - {self.amount}"

    def save(self, *args, **kwargs):
        if not self.payment_number:
            self.payment_number = self.generate_payment_number()
        
        super().save(*args, **kwargs)
        
        self.sale.paid_amount = self.sale.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        self.sale.save()

    def generate_payment_number(self):
        from django.utils import timezone
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        return f"PAY-{timestamp}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            related_name='carts', verbose_name=_('user'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='carts', verbose_name=_('customer'))
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Cart {self.id} - {self.user.email}"

    @property
    def total_items(self):
        return self.cart_items.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.cart_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, 
                            related_name='cart_items', verbose_name=_('cart'))
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, 
                                      related_name='cart_items', verbose_name=_('inventory item'))
    
    quantity = models.IntegerField(_('quantity'), default=1)
    price_at_addition = models.DecimalField(_('price at addition'), max_digits=10, decimal_places=2)
    
    added_at = models.DateTimeField(_('added at'), auto_now_add=True)

    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')
        ordering = ['-added_at']
        unique_together = ['cart', 'inventory_item']

    def __str__(self):
        return f"{self.inventory_item.part.name} x{self.quantity}"

    def save(self, *args, **kwargs):
        if not self.price_at_addition:
            self.price_at_addition = self.inventory_item.selling_price
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.price_at_addition * self.quantity
