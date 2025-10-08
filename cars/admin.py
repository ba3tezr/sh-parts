from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CarMake, CarModel, PartCategory, Part, Vehicle, VehiclePhoto


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'name_ar')
    ordering = ('name',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'name', 'year_start', 'year_end', 'body_type', 'is_active')
    list_filter = ('make', 'is_active', 'body_type')
    search_fields = ('name', 'name_ar', 'make__name')
    ordering = ('make', 'name')


@admin.register(PartCategory)
class PartCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'sort_order', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'name_ar')
    ordering = ('sort_order', 'name')


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'part_number', 'is_universal', 'is_active')
    list_filter = ('category', 'is_universal', 'is_active')
    search_fields = ('name', 'name_ar', 'part_number')
    filter_horizontal = ('compatible_models',)
    ordering = ('category', 'name')


class VehiclePhotoInline(admin.TabularInline):
    model = VehiclePhoto
    extra = 1


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vin', 'make', 'model', 'year', 'condition', 'intake_date', 'is_dismantled')
    list_filter = ('make', 'condition', 'is_dismantled', 'intake_date')
    search_fields = ('vin', 'make__name', 'model__name')
    date_hierarchy = 'intake_date'
    inlines = [VehiclePhotoInline]
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Vehicle Information'), {
            'fields': ('vin', 'make', 'model', 'year', 'color', 'mileage', 'condition')
        }),
        (_('Intake Details'), {
            'fields': ('intake_notes', 'purchase_price', 'received_by')
        }),
        (_('Dismantling Status'), {
            'fields': ('is_dismantled', 'dismantled_date')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
