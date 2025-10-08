from rest_framework import serializers
from .models import CarMake, CarModel, PartCategory, Part, Vehicle, VehiclePhoto


class CarMakeSerializer(serializers.ModelSerializer):
    models_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CarMake
        fields = ['id', 'name', 'name_ar', 'logo', 'is_active', 'models_count', 'created_at']
        
    def get_models_count(self, obj):
        return obj.models.filter(is_active=True).count()


class CarModelSerializer(serializers.ModelSerializer):
    make_name = serializers.CharField(source='make.name', read_only=True)
    make_name_ar = serializers.CharField(source='make.name_ar', read_only=True)
    compatible_parts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CarModel
        fields = ['id', 'make', 'make_name', 'make_name_ar', 'name', 'name_ar', 
                 'year_start', 'year_end', 'body_type', 'is_active', 'compatible_parts_count']
    
    def get_compatible_parts_count(self, obj):
        return obj.compatible_parts.filter(is_active=True).count()


class PartCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    parts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PartCategory
        fields = ['id', 'name', 'name_ar', 'parent', 'parent_name', 'description', 
                 'icon', 'sort_order', 'is_active', 'subcategories', 'parts_count']
    
    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return PartCategorySerializer(obj.subcategories.filter(is_active=True), many=True).data
        return []
    
    def get_parts_count(self, obj):
        return obj.parts.filter(is_active=True).count()


class PartListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_name_ar = serializers.CharField(source='category.name_ar', read_only=True)
    
    class Meta:
        model = Part
        fields = ['id', 'name', 'name_ar', 'category', 'category_name', 'category_name_ar',
                 'part_number', 'is_universal', 'default_image']


class PartDetailSerializer(serializers.ModelSerializer):
    category_details = PartCategorySerializer(source='category', read_only=True)
    compatible_models_details = CarModelSerializer(source='compatible_models', many=True, read_only=True)
    inventory_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Part
        fields = ['id', 'name', 'name_ar', 'category', 'category_details', 'part_number',
                 'description', 'description_ar', 'compatible_models', 'compatible_models_details',
                 'default_image', 'is_universal', 'is_active', 'inventory_count', 'created_at']
    
    def get_inventory_count(self, obj):
        return obj.inventory_items.filter(status='AVAILABLE').count()


class VehiclePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiclePhoto
        fields = ['id', 'image', 'caption', 'is_primary', 'uploaded_at']


class VehicleSerializer(serializers.ModelSerializer):
    make_name = serializers.CharField(source='make.name', read_only=True)
    model_name = serializers.CharField(source='model.name', read_only=True)
    received_by_name = serializers.CharField(source='received_by.get_full_name', read_only=True)
    photos = VehiclePhotoSerializer(many=True, read_only=True)
    extracted_parts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = ['id', 'vin', 'make', 'make_name', 'model', 'model_name', 'year', 
                 'color', 'mileage', 'condition', 'intake_date', 'intake_notes', 
                 'purchase_price', 'received_by', 'received_by_name', 'is_dismantled', 
                 'dismantled_date', 'photos', 'extracted_parts_count', 'created_at']
    
    def get_extracted_parts_count(self, obj):
        return obj.extracted_parts.count()


class VehicleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['vin', 'make', 'model', 'year', 'color', 'mileage', 'condition',
                 'intake_notes', 'purchase_price', 'received_by']
