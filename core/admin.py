from django.contrib import admin
from .models import SystemSettings


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('معلومات الشركة', {
            'fields': ('company_name', 'company_name_en')
        }),
        ('إعدادات العملة والمنطقة', {
            'fields': ('currency', 'default_language', 'timezone')
        }),
        ('إعدادات الضرائب', {
            'fields': ('tax_enabled', 'tax_rate', 'tax_number')
        }),
        ('معلومات الاتصال', {
            'fields': ('phone', 'email', 'address', 'city', 'country')
        }),
        ('إعدادات المخزون', {
            'fields': ('low_stock_threshold', 'allow_negative_stock')
        }),
        ('إعدادات المبيعات', {
            'fields': ('require_customer_for_sale',)
        }),
    )
    
    def has_add_permission(self, request):
        # السماح بإضافة إعدادات فقط إذا لم يكن هناك إعدادات موجودة
        return SystemSettings.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        # منع حذف الإعدادات
        return False
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
