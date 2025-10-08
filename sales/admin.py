from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Sale, SaleItem, Payment, Cart, CartItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('total_price',)


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('payment_number', 'payment_date')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'status', 'payment_status', 'total_amount', 
                   'paid_amount', 'balance_due', 'sales_person', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('invoice_number', 'customer__customer_code', 'customer__first_name', 
                    'customer__last_name')
    date_hierarchy = 'created_at'
    readonly_fields = ('invoice_number', 'subtotal', 'total_amount', 'balance_due', 
                      'created_at', 'updated_at', 'completed_at')
    inlines = [SaleItemInline, PaymentInline]
    
    fieldsets = (
        (_('Sale Information'), {
            'fields': ('invoice_number', 'customer', 'status', 'payment_status', 'sales_person')
        }),
        (_('Pricing'), {
            'fields': ('subtotal', 'discount_amount', 'tax_amount', 'total_amount', 'paid_amount')
        }),
        (_('Additional'), {
            'fields': ('notes',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'inventory_item', 'quantity', 'unit_price', 'discount_amount', 'total_price')
    list_filter = ('sale__created_at',)
    search_fields = ('sale__invoice_number', 'inventory_item__sku', 'inventory_item__part__name')
    readonly_fields = ('total_price',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'sale', 'amount', 'payment_method', 'received_by', 'payment_date')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('payment_number', 'sale__invoice_number', 'reference_number')
    date_hierarchy = 'payment_date'
    readonly_fields = ('payment_number', 'payment_date')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('total_price', 'added_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer', 'total_items', 'total_amount', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__email', 'customer__customer_code')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'inventory_item', 'quantity', 'price_at_addition', 'total_price', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('cart__user__email', 'inventory_item__sku')
    readonly_fields = ('added_at',)
