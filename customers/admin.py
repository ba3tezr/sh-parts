from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Customer, CustomerCredit, CustomerNote


class CustomerCreditInline(admin.TabularInline):
    model = CustomerCredit
    extra = 0
    readonly_fields = ('issued_at', 'used_at')


class CustomerNoteInline(admin.TabularInline):
    model = CustomerNote
    extra = 1
    readonly_fields = ('created_at',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_code', 'get_full_name', 'customer_type', 'phone', 'email', 
                   'credit_limit', 'is_active', 'created_at')
    list_filter = ('customer_type', 'is_active', 'created_at', 'city', 'country')
    search_fields = ('customer_code', 'first_name', 'last_name', 'business_name', 
                    'email', 'phone', 'tax_id')
    readonly_fields = ('customer_code', 'created_at', 'updated_at')
    inlines = [CustomerCreditInline, CustomerNoteInline]
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('customer_code', 'customer_type', 'first_name', 'last_name', 'business_name')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'phone_secondary')
        }),
        (_('Address'), {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        (_('Financial'), {
            'fields': ('tax_id', 'credit_limit')
        }),
        (_('Additional'), {
            'fields': ('notes', 'is_active', 'created_by')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CustomerCredit)
class CustomerCreditAdmin(admin.ModelAdmin):
    list_display = ('customer', 'credit_amount', 'is_used', 'issued_at', 'issued_by')
    list_filter = ('is_used', 'issued_at')
    search_fields = ('customer__customer_code', 'customer__first_name', 'customer__last_name', 'reference')
    readonly_fields = ('issued_at', 'used_at')


@admin.register(CustomerNote)
class CustomerNoteAdmin(admin.ModelAdmin):
    list_display = ('customer', 'note_preview', 'is_important', 'created_by', 'created_at')
    list_filter = ('is_important', 'created_at')
    search_fields = ('customer__customer_code', 'customer__first_name', 'customer__last_name', 'note')
    readonly_fields = ('created_at',)
    
    def note_preview(self, obj):
        return obj.note[:50] + '...' if len(obj.note) > 50 else obj.note
    note_preview.short_description = _('Note')
