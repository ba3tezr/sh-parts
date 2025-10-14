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
    invoice_number = serializers.CharField(read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    balance_due = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    payment_status = serializers.CharField(read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'invoice_number', 'customer', 'discount_amount', 'tax_amount', 'notes',
                 'sales_person', 'items', 'total_amount', 'subtotal', 'paid_amount',
                 'balance_due', 'payment_status']
        read_only_fields = ['id', 'invoice_number', 'total_amount', 'subtotal', 'paid_amount',
                           'balance_due', 'payment_status']

    def create(self, validated_data):
        from django.db import transaction

        items_data = validated_data.pop('items')

        with transaction.atomic():
            # إنشاء الطلب
            sale = Sale.objects.create(**validated_data)

            # إنشاء عناصر الطلب وحجز القطع
            for item_data in items_data:
                # إنشاء عنصر الطلب
                sale_item = SaleItem.objects.create(sale=sale, **item_data)

                # حجز القطعة في المخزون (تغيير الحالة إلى RESERVED)
                inventory_item = sale_item.inventory_item

                # التحقق من توفر الكمية
                if inventory_item.quantity < sale_item.quantity:
                    raise serializers.ValidationError({
                        'items': f'الكمية المطلوبة ({sale_item.quantity}) أكبر من المتوفر ({inventory_item.quantity}) للقطعة {inventory_item.part.name_ar}'
                    })

                # تغيير حالة القطعة إلى RESERVED
                if inventory_item.status == 'AVAILABLE':
                    inventory_item.status = 'RESERVED'
                    inventory_item.save()

            # ✅ إعادة حساب الإجماليات بعد إضافة العناصر
            sale.calculate_totals()
            sale.save()

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

    def create(self, validated_data):
        # ✅ إضافة received_by تلقائياً من المستخدم الحالي
        if 'received_by' not in validated_data:
            validated_data['received_by'] = self.context['request'].user

        payment = super().create(validated_data)

        # ✅ تحديث حالة الدفع للطلب
        payment.sale.update_payment_status()
        payment.sale.save()

        return payment


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
