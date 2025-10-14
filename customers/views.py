from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q, Avg, F, Max, Min, Case, When, Value, IntegerField
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
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

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get customer statistics for dashboard"""
        from sales.models import Sale

        # Date ranges
        now = timezone.now()
        month_ago = now - timedelta(days=30)
        week_ago = now - timedelta(days=7)
        year_ago = now - timedelta(days=365)

        # Total customers
        total_customers = Customer.objects.count()
        active_customers = Customer.objects.filter(is_active=True).count()

        # New customers
        new_this_month = Customer.objects.filter(created_at__gte=month_ago).count()
        new_this_week = Customer.objects.filter(created_at__gte=week_ago).count()

        # Sales data
        total_sales = Sale.objects.filter(
            customer__isnull=False
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )

        # Outstanding balance (unpaid and partial sales)
        outstanding = Sale.objects.filter(
            customer__isnull=False,
            payment_status__in=['UNPAID', 'PARTIAL']
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # Average customer value
        avg_customer_value = Sale.objects.filter(
            customer__isnull=False
        ).values('customer').annotate(
            total=Sum('total_amount')
        ).aggregate(
            avg=Avg('total')
        )['avg'] or 0

        # Customer types distribution
        customer_types = Customer.objects.values('customer_type').annotate(
            count=Count('id')
        )

        # Top customers
        top_customers = Sale.objects.filter(
            customer__isnull=False
        ).values(
            'customer__id',
            'customer__customer_code',
            'customer__first_name',
            'customer__last_name',
            'customer__business_name'
        ).annotate(
            total_purchases=Sum('total_amount'),
            purchase_count=Count('id')
        ).order_by('-total_purchases')[:10]

        # Customers at risk (no purchase in 90 days)
        from django.db.models import Max
        ninety_days_ago = now - timedelta(days=90)
        at_risk_customers = Customer.objects.filter(
            is_active=True,
            sales__isnull=False
        ).annotate(
            last_purchase=Max('sales__created_at')
        ).filter(
            last_purchase__lt=ninety_days_ago
        ).count()

        return Response({
            'total_customers': total_customers,
            'active_customers': active_customers,
            'inactive_customers': total_customers - active_customers,
            'new_this_month': new_this_month,
            'new_this_week': new_this_week,
            'total_sales_amount': total_sales['total'] or 0,
            'total_sales_count': total_sales['count'] or 0,
            'outstanding_balance': outstanding,
            'avg_customer_value': round(float(avg_customer_value), 2),
            'customer_types': list(customer_types),
            'top_customers': list(top_customers),
            'at_risk_customers': at_risk_customers,
        })

    @action(detail=False, methods=['get'])
    def cities(self, request):
        """Get list of cities for filter"""
        cities = Customer.objects.exclude(
            city__isnull=True
        ).exclude(
            city=''
        ).values_list('city', flat=True).distinct().order_by('city')
        return Response(list(cities))

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get comprehensive dashboard statistics"""
        from sales.models import Sale, Payment
        from django.db.models import Max, Min

        now = timezone.now()
        month_ago = now - timedelta(days=30)
        week_ago = now - timedelta(days=7)
        year_ago = now - timedelta(days=365)

        # Basic counts
        total_customers = Customer.objects.count()
        active_customers = Customer.objects.filter(is_active=True).count()
        individual_customers = Customer.objects.filter(customer_type='INDIVIDUAL').count()
        business_customers = Customer.objects.filter(customer_type='BUSINESS').count()

        # Growth metrics
        new_this_month = Customer.objects.filter(created_at__gte=month_ago).count()
        new_this_week = Customer.objects.filter(created_at__gte=week_ago).count()
        new_this_year = Customer.objects.filter(created_at__gte=year_ago).count()

        # Sales metrics
        total_sales = Sale.objects.filter(status='COMPLETED').aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )

        # Customer value metrics
        customers_with_purchases = Customer.objects.annotate(
            purchase_total=Sum('sales__total_amount', filter=Q(sales__status='COMPLETED'))
        ).filter(purchase_total__gt=0)

        avg_customer_value = customers_with_purchases.aggregate(
            avg=Avg('purchase_total')
        )['avg'] or 0

        # Top customers
        top_customers = list(customers_with_purchases.order_by('-purchase_total')[:10].values(
            'id', 'customer_code', 'first_name', 'last_name', 'business_name',
            'customer_type', 'purchase_total'
        ))

        # Outstanding balances
        customers_with_debt = Customer.objects.annotate(
            debt=Sum('sales__total_amount', filter=Q(sales__payment_status__in=['PARTIAL', 'UNPAID'])) -
                 Sum('sales__paid_amount', filter=Q(sales__payment_status__in=['PARTIAL', 'UNPAID']))
        ).filter(debt__gt=0)

        total_outstanding = customers_with_debt.aggregate(total=Sum('debt'))['total'] or 0
        customers_with_debt_count = customers_with_debt.count()

        # RFM Analysis (Recency, Frequency, Monetary)
        rfm_data = []
        for customer in Customer.objects.all()[:100]:  # Limit for performance
            last_purchase = Sale.objects.filter(
                customer=customer,
                status='COMPLETED'
            ).aggregate(last=Max('created_at'))['last']

            if last_purchase:
                recency = (now - last_purchase).days
                frequency = Sale.objects.filter(customer=customer, status='COMPLETED').count()
                monetary = Sale.objects.filter(
                    customer=customer,
                    status='COMPLETED'
                ).aggregate(total=Sum('total_amount'))['total'] or 0

                rfm_data.append({
                    'customer_id': customer.id,
                    'customer_code': customer.customer_code,
                    'customer_name': customer.get_full_name(),
                    'recency': recency,
                    'frequency': frequency,
                    'monetary': float(monetary)
                })

        # Monthly sales trend
        monthly_sales = []
        for i in range(12):
            month_start = now - timedelta(days=30 * (i + 1))
            month_end = now - timedelta(days=30 * i)
            month_total = Sale.objects.filter(
                status='COMPLETED',
                created_at__gte=month_start,
                created_at__lt=month_end
            ).aggregate(total=Sum('total_amount'))['total'] or 0

            monthly_sales.insert(0, {
                'month': month_start.strftime('%b %Y'),
                'total': float(month_total)
            })

        # Customer acquisition trend
        monthly_customers = []
        for i in range(12):
            month_start = now - timedelta(days=30 * (i + 1))
            month_end = now - timedelta(days=30 * i)
            month_count = Customer.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count()

            monthly_customers.insert(0, {
                'month': month_start.strftime('%b %Y'),
                'count': month_count
            })

        return Response({
            'total_customers': total_customers,
            'active_customers': active_customers,
            'inactive_customers': total_customers - active_customers,
            'individual_customers': individual_customers,
            'business_customers': business_customers,
            'new_this_month': new_this_month,
            'new_this_week': new_this_week,
            'new_this_year': new_this_year,
            'total_sales_amount': float(total_sales['total'] or 0),
            'total_sales_count': total_sales['count'],
            'avg_customer_value': round(float(avg_customer_value), 2),
            'total_outstanding': float(total_outstanding),
            'customers_with_debt_count': customers_with_debt_count,
            'top_customers': top_customers,
            'rfm_data': rfm_data,
            'monthly_sales': monthly_sales,
            'monthly_customers': monthly_customers
        })


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

    @action(detail=False, methods=['get'])
    def analytics_report(self, request):
        """تقرير تحليل العملاء - Customer Analytics Report"""
        from sales.models import Sale, Payment

        # Get date range from query params
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_date = timezone.now() - timedelta(days=365)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date = timezone.now()

        # Get all customers with their sales data
        customers = Customer.objects.annotate(
            total_sales=Sum('sales__total_amount', filter=Q(sales__created_at__range=[start_date, end_date])),
            sales_count=Count('sales', filter=Q(sales__created_at__range=[start_date, end_date])),
            last_purchase=Max('sales__created_at'),
            first_purchase=Min('sales__created_at')
        ).filter(sales_count__gt=0)

        # Calculate RFM scores
        now = timezone.now()
        rfm_data = []

        for customer in customers:
            if customer.last_purchase:
                recency = (now - customer.last_purchase).days
                frequency = customer.sales_count or 0
                monetary = float(customer.total_sales or 0)

                # Calculate RFM scores (1-5 scale)
                r_score = 5 if recency <= 30 else (4 if recency <= 60 else (3 if recency <= 90 else (2 if recency <= 180 else 1)))
                f_score = 5 if frequency >= 10 else (4 if frequency >= 7 else (3 if frequency >= 5 else (2 if frequency >= 3 else 1)))
                m_score = 5 if monetary >= 10000 else (4 if monetary >= 5000 else (3 if monetary >= 2000 else (2 if monetary >= 1000 else 1)))

                rfm_score = r_score + f_score + m_score

                # Segment classification
                if rfm_score >= 13:
                    segment = 'Champions'
                elif rfm_score >= 10:
                    segment = 'Loyal Customers'
                elif rfm_score >= 7:
                    segment = 'Potential Loyalists'
                elif rfm_score >= 5:
                    segment = 'At Risk'
                else:
                    segment = 'Lost'

                # Calculate CLV (Customer Lifetime Value)
                if customer.first_purchase:
                    customer_age_days = (now - customer.first_purchase).days
                    if customer_age_days > 0:
                        avg_purchase_value = monetary / frequency if frequency > 0 else 0
                        purchase_frequency = frequency / (customer_age_days / 30) if customer_age_days > 0 else 0
                        customer_lifespan = 36  # Assume 3 years
                        clv = avg_purchase_value * purchase_frequency * customer_lifespan
                    else:
                        clv = monetary
                else:
                    clv = monetary

                rfm_data.append({
                    'customer_id': customer.id,
                    'customer_code': customer.customer_code,
                    'customer_name': f"{customer.first_name} {customer.last_name}",
                    'recency': recency,
                    'frequency': frequency,
                    'monetary': monetary,
                    'r_score': r_score,
                    'f_score': f_score,
                    'm_score': m_score,
                    'rfm_score': rfm_score,
                    'segment': segment,
                    'clv': round(clv, 2),
                    'last_purchase': customer.last_purchase.strftime('%Y-%m-%d') if customer.last_purchase else None
                })

        # Sort by RFM score
        rfm_data.sort(key=lambda x: x['rfm_score'], reverse=True)

        # Calculate segment distribution
        segment_distribution = {}
        for item in rfm_data:
            segment = item['segment']
            if segment not in segment_distribution:
                segment_distribution[segment] = {'count': 0, 'total_value': 0}
            segment_distribution[segment]['count'] += 1
            segment_distribution[segment]['total_value'] += item['monetary']

        # Calculate retention rate
        total_customers = Customer.objects.count()
        active_customers = customers.count()
        retention_rate = (active_customers / total_customers * 100) if total_customers > 0 else 0

        return Response({
            'rfm_analysis': rfm_data,
            'segment_distribution': segment_distribution,
            'retention_rate': round(retention_rate, 2),
            'total_customers_analyzed': len(rfm_data),
            'date_range': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')
            }
        })

    @action(detail=False, methods=['get'])
    def debt_report(self, request):
        """تقرير الديون - Debt Report"""
        from sales.models import Sale

        # Get customers with outstanding balance
        customers_with_debt = Customer.objects.annotate(
            total_sales=Sum('sales__total_amount'),
            total_paid=Sum('sales__payments__amount'),
            outstanding=F('total_sales') - F('total_paid')
        ).filter(outstanding__gt=0).order_by('-outstanding')

        debt_data = []
        aging_buckets = {
            '0-30': {'count': 0, 'amount': 0},
            '31-60': {'count': 0, 'amount': 0},
            '61-90': {'count': 0, 'amount': 0},
            '90+': {'count': 0, 'amount': 0}
        }

        now = timezone.now()
        total_debt = 0

        for customer in customers_with_debt:
            outstanding = float(customer.outstanding or 0)
            if outstanding <= 0:
                continue

            # Get oldest unpaid sale
            oldest_sale = Sale.objects.filter(
                customer=customer,
                payment_status__in=['UNPAID', 'PARTIAL']
            ).order_by('created_at').first()

            if oldest_sale:
                days_overdue = (now - oldest_sale.created_at).days

                # Determine aging bucket
                if days_overdue <= 30:
                    bucket = '0-30'
                elif days_overdue <= 60:
                    bucket = '31-60'
                elif days_overdue <= 90:
                    bucket = '61-90'
                else:
                    bucket = '90+'

                aging_buckets[bucket]['count'] += 1
                aging_buckets[bucket]['amount'] += outstanding
            else:
                days_overdue = 0
                bucket = '0-30'

            total_debt += outstanding

            debt_data.append({
                'customer_id': customer.id,
                'customer_code': customer.customer_code,
                'customer_name': f"{customer.first_name} {customer.last_name}",
                'customer_type': customer.customer_type,
                'outstanding_balance': outstanding,
                'credit_limit': float(customer.credit_limit),
                'days_overdue': days_overdue,
                'aging_bucket': bucket,
                'phone': customer.phone,
                'email': customer.email
            })

        return Response({
            'debt_details': debt_data,
            'aging_analysis': aging_buckets,
            'total_debt': round(total_debt, 2),
            'customers_with_debt': len(debt_data),
            'high_risk_customers': len([d for d in debt_data if d['days_overdue'] > 90])
        })

    @action(detail=False, methods=['get'])
    def sales_report(self, request):
        """تقرير مبيعات العملاء - Customer Sales Report"""
        from sales.models import Sale

        # Get date range
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_date = timezone.now() - timedelta(days=365)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date = timezone.now()

        # Get customers with sales data
        customers = Customer.objects.annotate(
            total_sales=Sum('sales__total_amount', filter=Q(sales__created_at__range=[start_date, end_date])),
            sales_count=Count('sales', filter=Q(sales__created_at__range=[start_date, end_date])),
            avg_sale_value=Avg('sales__total_amount', filter=Q(sales__created_at__range=[start_date, end_date])),
            last_sale=Max('sales__created_at', filter=Q(sales__created_at__range=[start_date, end_date]))
        ).filter(sales_count__gt=0).order_by('-total_sales')

        sales_data = []
        total_revenue = 0

        for customer in customers:
            total_sales = float(customer.total_sales or 0)
            total_revenue += total_sales

            # Calculate profitability (simplified - would need cost data for accurate calculation)
            # Assuming 30% profit margin
            estimated_profit = total_sales * 0.3

            sales_data.append({
                'customer_id': customer.id,
                'customer_code': customer.customer_code,
                'customer_name': f"{customer.first_name} {customer.last_name}",
                'customer_type': customer.customer_type,
                'total_sales': total_sales,
                'sales_count': customer.sales_count,
                'avg_sale_value': float(customer.avg_sale_value or 0),
                'estimated_profit': round(estimated_profit, 2),
                'profit_margin': 30.0,
                'last_sale': customer.last_sale.strftime('%Y-%m-%d') if customer.last_sale else None
            })

        # Calculate revenue distribution
        if total_revenue > 0:
            for item in sales_data:
                item['revenue_percentage'] = round((item['total_sales'] / total_revenue) * 100, 2)

        # Top 10 customers
        top_10 = sales_data[:10]

        # Calculate 80/20 rule (Pareto principle)
        cumulative_revenue = 0
        customers_for_80_percent = 0
        for item in sales_data:
            cumulative_revenue += item['total_sales']
            customers_for_80_percent += 1
            if cumulative_revenue >= total_revenue * 0.8:
                break

        return Response({
            'sales_by_customer': sales_data,
            'top_10_customers': top_10,
            'total_revenue': round(total_revenue, 2),
            'total_customers': len(sales_data),
            'avg_revenue_per_customer': round(total_revenue / len(sales_data), 2) if len(sales_data) > 0 else 0,
            'pareto_analysis': {
                'customers_for_80_percent': customers_for_80_percent,
                'percentage': round((customers_for_80_percent / len(sales_data)) * 100, 2) if len(sales_data) > 0 else 0
            },
            'date_range': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')
            }
        })

    @action(detail=False, methods=['get'])
    def loyalty_report(self, request):
        """تقرير الولاء - Loyalty Report"""
        from sales.models import Sale

        # Get all customers with purchase history
        customers = Customer.objects.annotate(
            total_purchases=Sum('sales__total_amount'),
            purchase_count=Count('sales'),
            first_purchase=Min('sales__created_at'),
            last_purchase=Max('sales__created_at')
        ).filter(purchase_count__gt=0)

        loyalty_data = []
        now = timezone.now()

        for customer in customers:
            if not customer.first_purchase:
                continue

            # Calculate customer tenure
            tenure_days = (now - customer.first_purchase).days
            tenure_months = tenure_days / 30

            # Calculate purchase frequency
            if tenure_months > 0:
                purchases_per_month = customer.purchase_count / tenure_months
            else:
                purchases_per_month = customer.purchase_count

            # Calculate loyalty score (0-100)
            # Based on: tenure (40%), frequency (30%), monetary (30%)
            tenure_score = min(tenure_months / 12 * 40, 40)  # Max 40 points for 1 year+
            frequency_score = min(purchases_per_month * 10, 30)  # Max 30 points
            monetary_score = min(float(customer.total_purchases or 0) / 1000 * 3, 30)  # Max 30 points

            loyalty_score = tenure_score + frequency_score + monetary_score

            # Determine loyalty tier
            if loyalty_score >= 80:
                tier = 'Platinum'
            elif loyalty_score >= 60:
                tier = 'Gold'
            elif loyalty_score >= 40:
                tier = 'Silver'
            else:
                tier = 'Bronze'

            # Calculate repeat rate
            repeat_rate = ((customer.purchase_count - 1) / customer.purchase_count * 100) if customer.purchase_count > 1 else 0

            # Days since last purchase
            days_since_last = (now - customer.last_purchase).days if customer.last_purchase else 0

            # Status
            if days_since_last <= 30:
                status = 'Active'
            elif days_since_last <= 90:
                status = 'At Risk'
            else:
                status = 'Inactive'

            loyalty_data.append({
                'customer_id': customer.id,
                'customer_code': customer.customer_code,
                'customer_name': f"{customer.first_name} {customer.last_name}",
                'loyalty_score': round(loyalty_score, 2),
                'tier': tier,
                'tenure_months': round(tenure_months, 1),
                'total_purchases': float(customer.total_purchases or 0),
                'purchase_count': customer.purchase_count,
                'purchases_per_month': round(purchases_per_month, 2),
                'repeat_rate': round(repeat_rate, 2),
                'days_since_last_purchase': days_since_last,
                'status': status,
                'first_purchase': customer.first_purchase.strftime('%Y-%m-%d'),
                'last_purchase': customer.last_purchase.strftime('%Y-%m-%d') if customer.last_purchase else None
            })

        # Sort by loyalty score
        loyalty_data.sort(key=lambda x: x['loyalty_score'], reverse=True)

        # Calculate tier distribution
        tier_distribution = {
            'Platinum': {'count': 0, 'total_value': 0},
            'Gold': {'count': 0, 'total_value': 0},
            'Silver': {'count': 0, 'total_value': 0},
            'Bronze': {'count': 0, 'total_value': 0}
        }

        for item in loyalty_data:
            tier = item['tier']
            tier_distribution[tier]['count'] += 1
            tier_distribution[tier]['total_value'] += item['total_purchases']

        # Calculate status distribution
        status_distribution = {
            'Active': 0,
            'At Risk': 0,
            'Inactive': 0
        }

        for item in loyalty_data:
            status_distribution[item['status']] += 1

        return Response({
            'loyalty_analysis': loyalty_data,
            'tier_distribution': tier_distribution,
            'status_distribution': status_distribution,
            'total_customers': len(loyalty_data),
            'avg_loyalty_score': round(sum(item['loyalty_score'] for item in loyalty_data) / len(loyalty_data), 2) if len(loyalty_data) > 0 else 0
        })
