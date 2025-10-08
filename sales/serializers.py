from rest_framework import serializers
from .models import Sale, SaleItem, Payment, Cart, CartItem
from customers.serializers import CustomerListSerializer
from inventory.serializers import InventoryItemListSerializer


class SaleItemSerializer(serializers.ModelSerializer):
    inventory_item_details = InventoryItemListSerializer(source='inventory_item', read_only=True)
    part_name = serializers.CharField(source='inventory_item.part.name', read_only=True)
    
    class Meta:
        model = SaleItem
        fields = ['id', 'inventory_item', 'inventory_item_details', 'part_name',
                 'quantity', 'unit_price', 'discount_percent', 'discount_amount', 
                 'total_price', 'notes']


class SaleListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    sales_person_name = serializers.CharField(source='sales_person.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Sale
        fields = ['id', 'invoice_number', 'customer', 'customer_name', 'status', 
                 'status_display', 'payment_status', 'payment_status_display', 
                 'total_amount', 'paid_amount', 'balance_due', 'sales_person', 
                 'sales_person_name', 'created_at']


class SaleDetailSerializer(serializers.ModelSerializer):
    customer_details = CustomerListSerializer(source='customer', read_only=True)
    sales_person_name = serializers.CharField(source='sales_person.get_full_name', read_only=True)
    items = SaleItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Sale
        fields = ['id', 'invoice_number', 'customer', 'customer_details', 'status', 
                 'status_display', 'payment_status', 'payment_status_display', 'subtotal',
                 'discount_amount', 'tax_amount', 'total_amount', 'paid_amount', 'balance_due',
                 'notes', 'sales_person', 'sales_person_name', 'items', 'created_at', 
                 'updated_at', 'completed_at']


class SaleCreateSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    
    class Meta:
        model = Sale
        fields = ['customer', 'discount_amount', 'tax_amount', 'notes', 'sales_person', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        
        for item_data in items_data:
            SaleItem.objects.create(sale=sale, **item_data)
        
        return sale


class PaymentSerializer(serializers.ModelSerializer):
    sale_invoice = serializers.CharField(source='sale.invoice_number', read_only=True)
    received_by_name = serializers.CharField(source='received_by.get_full_name', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'payment_number', 'sale', 'sale_invoice', 'amount', 
                 'payment_method', 'payment_method_display', 'reference_number', 
                 'notes', 'received_by', 'received_by_name', 'payment_date']


class CartItemSerializer(serializers.ModelSerializer):
    inventory_item_details = InventoryItemListSerializer(source='inventory_item', read_only=True)
    part_name = serializers.CharField(source='inventory_item.part.name', read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'inventory_item', 'inventory_item_details', 'part_name',
                 'quantity', 'price_at_addition', 'total_price', 'added_at']


class CartSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    cart_items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'user_name', 'customer', 'customer_name', 
                 'total_items', 'total_amount', 'cart_items', 'is_active', 
                 'created_at', 'updated_at']
