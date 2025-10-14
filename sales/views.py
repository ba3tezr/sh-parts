from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from .models import Sale, SaleItem, Payment, Cart, CartItem
from .serializers import (
    SaleListSerializer, SaleDetailSerializer, SaleCreateSerializer,
    SaleItemSerializer, PaymentSerializer, CartSerializer, CartItemSerializer
)


class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Sale.objects.select_related('customer', 'sales_person').prefetch_related('items').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer', 'status', 'payment_status', 'sales_person']
    search_fields = ['invoice_number', 'customer__customer_code', 'customer__first_name', 
                    'customer__last_name']
    ordering_fields = ['created_at', 'total_amount', 'invoice_number']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SaleDetailSerializer
        elif self.action == 'create':
            return SaleCreateSerializer
        return SaleListSerializer
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a draft sale"""
        sale = self.get_object()
        if sale.status != 'DRAFT':
            return Response(
                {'error': 'Only draft sales can be confirmed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sale.status = 'CONFIRMED'
        sale.save()
        
        serializer = self.get_serializer(sale)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a sale"""
        from django.utils import timezone
        
        sale = self.get_object()
        if sale.status not in ['DRAFT', 'CONFIRMED']:
            return Response(
                {'error': 'Sale is already completed or cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Update inventory items
            for item in sale.items.all():
                inventory_item = item.inventory_item
                if inventory_item.quantity < item.quantity:
                    return Response(
                        {'error': f'Insufficient quantity for {inventory_item.part.name}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # خصم الكمية
                inventory_item.quantity -= item.quantity

                # تحديث الحالة
                if inventory_item.quantity == 0:
                    inventory_item.status = 'SOLD'
                else:
                    # إذا كانت محجوزة، نعيدها لمتوفرة بعد خصم الكمية
                    if inventory_item.status == 'RESERVED':
                        inventory_item.status = 'AVAILABLE'

                inventory_item.save()

                # Create stock movement
                from inventory.models import StockMovement
                StockMovement.objects.create(
                    item=inventory_item,
                    movement_type='OUT',
                    quantity=item.quantity,
                    reason=f'Sale {sale.invoice_number}',
                    reference=sale.invoice_number,
                    performed_by=request.user
                )

            sale.status = 'COMPLETED'
            sale.completed_at = timezone.now()
            sale.save()
        
        serializer = self.get_serializer(sale)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a sale and release reserved items"""
        sale = self.get_object()
        if sale.status == 'COMPLETED':
            return Response(
                {'error': 'Completed sales cannot be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # إلغاء حجز القطع
            for item in sale.items.all():
                inventory_item = item.inventory_item
                if inventory_item.status == 'RESERVED':
                    inventory_item.status = 'AVAILABLE'
                    inventory_item.save()

            # إلغاء الطلب
            sale.status = 'CANCELLED'
            sale.save()

        serializer = self.get_serializer(sale)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        """Get all payments for a sale"""
        sale = self.get_object()
        payments = sale.payments.all().order_by('-payment_date')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_payment(self, request, pk=None):
        """Add a payment for a sale"""
        sale = self.get_object()
        data = request.data.copy()
        data['sale'] = sale.id
        data['received_by'] = request.user.id
        
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Payment.objects.select_related('sale', 'received_by').all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sale', 'payment_method', 'received_by']
    search_fields = ['payment_number', 'reference_number', 'sale__invoice_number']
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CartSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'customer', 'is_active']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        # Users can only see their own carts
        return Cart.objects.filter(user=self.request.user).prefetch_related('cart_items')
    
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Add item to cart"""
        cart = self.get_object()
        data = request.data.copy()
        data['cart'] = cart.id
        
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """Remove item from cart"""
        cart = self.get_object()
        item_id = request.data.get('item_id')
        
        try:
            cart_item = cart.cart_items.get(id=item_id)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        """Clear all items from cart"""
        cart = self.get_object()
        cart.cart_items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        """Convert cart to sale"""
        cart = self.get_object()
        
        if not cart.cart_items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not cart.customer:
            return Response(
                {'error': 'Customer must be set before checkout'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Create sale
            sale = Sale.objects.create(
                customer=cart.customer,
                sales_person=request.user
            )
            
            # Create sale items from cart items
            for cart_item in cart.cart_items.all():
                SaleItem.objects.create(
                    sale=sale,
                    inventory_item=cart_item.inventory_item,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.price_at_addition
                )
            
            # Clear cart
            cart.is_active = False
            cart.save()
        
        serializer = SaleDetailSerializer(sale)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
