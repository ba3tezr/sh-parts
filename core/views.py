from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Count
from django.db import transaction
import json
from decimal import Decimal
from sales.models import Sale
from inventory.models import InventoryItem
from customers.models import Customer
from cars.models import Vehicle, CarMake


@login_required
def dashboard(request):
    """لوحة التحكم الرئيسية - Main Dashboard"""
    context = {
        'total_sales': Sale.objects.filter(status='COMPLETED').aggregate(
            total=Sum('total_amount')
        )['total'] or 0,
        'total_inventory': InventoryItem.objects.filter(status='AVAILABLE').count(),
        'total_customers': Customer.objects.filter(is_active=True).count(),
        'pending_orders': Sale.objects.filter(status__in=['DRAFT', 'CONFIRMED']).count(),
    }
    return render(request, 'pages/dashboard.html', context)


@login_required
def vehicles_list(request):
    """قائمة السيارات - Vehicles List"""
    vehicles = Vehicle.objects.all().select_related('make', 'model').order_by('-intake_date')
    context = {
        'vehicles': vehicles,
    }
    return render(request, 'pages/vehicles.html', context)


@login_required
def inventory_list(request):
    """قائمة المخزون - Inventory List"""
    items = InventoryItem.objects.all().select_related('part', 'location').order_by('-added_at')
    context = {
        'items': items,
    }
    return render(request, 'pages/inventory.html', context)


@login_required
def sales_list(request):
    """قائمة المبيعات - Sales List"""
    sales = Sale.objects.all().select_related('customer').order_by('-created_at')
    context = {
        'sales': sales,
    }
    return render(request, 'pages/sales.html', context)


@login_required
def customers_list(request):
    """قائمة العملاء - Customers List"""
    customers = Customer.objects.filter(is_active=True).order_by('-id')
    context = {
        'customers': customers,
    }
    return render(request, 'pages/customers.html', context)


@login_required
def reports_view(request):
    """التقارير - Reports"""
    return render(request, 'pages/reports.html')


def login_view(request):
    """صفحة تسجيل الدخول - Login Page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'البريد الإلكتروني أو كلمة المرور غير صحيحة')
    
    return render(request, 'pages/login.html')


def logout_view(request):
    """تسجيل الخروج - Logout"""
    logout(request)
    return redirect('login')

@login_required
def price_management_view(request):
    """صفحة إدارة الأسعار - للمدير فقط"""
    if not request.user.is_staff:
        return redirect('dashboard')
    
    return render(request, 'pages/price_management.html')


@login_required
def vehicle_dismantle_view(request, vehicle_id):
    """صفحة تفكيك السيارة مع Checklist"""
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    return render(request, 'pages/vehicle_dismantle.html', {
        'vehicle': vehicle
    })


@login_required
@require_http_methods(["POST"])
def save_dismantling(request):
    """حفظ عملية التفكيك وتدريج القطع في المخزون"""
    try:
        data = json.loads(request.body)
        vehicle_id = data.get('vehicle_id')
        parts = data.get('parts', [])
        
        from inventory.models import Part, StockMovement, Location
        
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        
        # التأكد من عدم التفكيك المسبق
        if vehicle.is_dismantled:
            return JsonResponse({
                'success': False,
                'message': 'هذه السيارة تم تفكيكها بالفعل'
            }, status=400)
        
        created_items = []
        
        with transaction.atomic():
            # الحصول على الموقع الافتراضي أو إنشاؤه
            default_location, _ = Location.objects.get_or_create(
                name='مخزن التفكيك',
                defaults={'location_type': 'WAREHOUSE'}
            )
            
            # معالجة كل قطعة
            for part_data in parts:
                # إنشاء أو الحصول على القطعة
                part, created = Part.objects.get_or_create(
                    name_ar=part_data['name_ar'],
                    defaults={
                        'name_en': part_data.get('name_en', ''),
                        'category': part_data.get('category', 'MISC'),
                        'description': f"قطعة من {vehicle.make.name} {vehicle.model.name} {vehicle.year}"
                    }
                )
                
                # إنشاء عنصر في المخزون
                inventory_item = InventoryItem.objects.create(
                    part=part,
                    vehicle_source=vehicle,
                    condition=part_data.get('condition', 'USED_GOOD'),
                    quantity=1,
                    selling_price=Decimal(str(part_data.get('price', 0))),
                    location=default_location,
                    status='AVAILABLE'
                )
                
                # إنشاء حركة مخزون
                StockMovement.objects.create(
                    inventory_item=inventory_item,
                    movement_type='IN',
                    quantity=1,
                    reference_number=f'DISMANTLE-{vehicle.id}',
                    notes=f'تفكيك سيارة: {vehicle.make.name} {vehicle.model.name} {vehicle.year}',
                    performed_by=request.user
                )
                
                created_items.append({
                    'id': inventory_item.id,
                    'sku': inventory_item.sku,
                    'part': part.name_ar,
                    'price': str(inventory_item.selling_price)
                })
            
            # تحديث حالة السيارة
            vehicle.is_dismantled = True
            vehicle.save()
        
        return JsonResponse({
            'success': True,
            'message': f'تم تفكيك السيارة بنجاح وإضافة {len(created_items)} قطعة إلى المخزون',
            'items': created_items
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'حدث خطأ: {str(e)}'
        }, status=500)
