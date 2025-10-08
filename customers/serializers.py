from rest_framework import serializers
from .models import Customer, CustomerCredit, CustomerNote


class CustomerListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    customer_type_display = serializers.CharField(source='get_customer_type_display', read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'customer_code', 'customer_type', 'customer_type_display',
                 'first_name', 'last_name', 'full_name', 'business_name', 'email', 
                 'phone', 'credit_limit', 'is_active', 'created_at']


class CustomerDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    customer_type_display = serializers.CharField(source='get_customer_type_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    total_purchases = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    outstanding_balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'customer_code', 'customer_type', 'customer_type_display', 
                 'first_name', 'last_name', 'full_name', 'business_name', 'email', 
                 'phone', 'phone_secondary', 'address_line1', 'address_line2', 'city', 
                 'state', 'postal_code', 'country', 'tax_id', 'credit_limit', 'notes', 
                 'is_active', 'created_by', 'created_by_name', 'total_purchases', 
                 'outstanding_balance', 'created_at', 'updated_at']


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_type', 'first_name', 'last_name', 'business_name', 'email',
                 'phone', 'phone_secondary', 'address_line1', 'address_line2', 'city',
                 'state', 'postal_code', 'country', 'tax_id', 'credit_limit', 'notes', 'created_by']


class CustomerCreditSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.get_full_name', read_only=True)
    
    class Meta:
        model = CustomerCredit
        fields = ['id', 'customer', 'customer_name', 'credit_amount', 'reason', 
                 'reference', 'issued_by', 'issued_by_name', 'is_used', 'issued_at', 'used_at']


class CustomerNoteSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = CustomerNote
        fields = ['id', 'customer', 'customer_name', 'note', 'is_important',
                 'created_by', 'created_by_name', 'created_at']
