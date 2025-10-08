from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, CustomerCredit, CustomerNote
from .serializers import (
    CustomerListSerializer, CustomerDetailSerializer, CustomerCreateSerializer,
    CustomerCreditSerializer, CustomerNoteSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Customer.objects.select_related('created_by').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer_type', 'is_active', 'city', 'country']
    search_fields = ['customer_code', 'first_name', 'last_name', 'business_name', 
                    'email', 'phone', 'tax_id']
    ordering_fields = ['customer_code', 'first_name', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CustomerDetailSerializer
        elif self.action == 'create':
            return CustomerCreateSerializer
        return CustomerListSerializer
    
    @action(detail=True, methods=['get'])
    def purchase_history(self, request, pk=None):
        """Get customer purchase history"""
        from sales.serializers import SaleListSerializer
        customer = self.get_object()
        sales = customer.sales.all().order_by('-created_at')
        serializer = SaleListSerializer(sales, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def credits(self, request, pk=None):
        """Get customer credits"""
        customer = self.get_object()
        credits = customer.credits.all().order_by('-issued_at')
        serializer = CustomerCreditSerializer(credits, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_credit(self, request, pk=None):
        """Add credit for customer"""
        customer = self.get_object()
        data = request.data.copy()
        data['customer'] = customer.id
        data['issued_by'] = request.user.id
        
        serializer = CustomerCreditSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def notes(self, request, pk=None):
        """Get customer notes"""
        customer = self.get_object()
        notes = customer.customer_notes.all().order_by('-created_at')
        serializer = CustomerNoteSerializer(notes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """Add note for customer"""
        customer = self.get_object()
        data = request.data.copy()
        data['customer'] = customer.id
        data['created_by'] = request.user.id
        
        serializer = CustomerNoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerCreditViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CustomerCredit.objects.select_related('customer', 'issued_by').all()
    serializer_class = CustomerCreditSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['customer', 'is_used', 'issued_by']
    ordering_fields = ['issued_at', 'credit_amount']
    ordering = ['-issued_at']


class CustomerNoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CustomerNote.objects.select_related('customer', 'created_by').all()
    serializer_class = CustomerNoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer', 'is_important', 'created_by']
    search_fields = ['note']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
