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
def inventory_enhanced(request):
    """قائمة المخزون المحسّنة - Enhanced Inventory List"""
    return render(request, 'pages/inventory_enhanced.html')


@login_required
def inventory_item_details(request):
    """تفاصيل القطعة - Item Details"""
    return render(request, 'pages/inventory_item_details.html')


@login_required
def profitability_report(request):
    """تقرير الربحية - Profitability Report"""
    return render(request, 'pages/profitability_report.html')


@login_required
def inventory_count(request):
    """نظام الجرد - Inventory Count"""
    return render(request, 'pages/inventory_count.html')


@login_required
def inventory_dashboard(request):
    """لوحة تحكم المخزون - Inventory Dashboard"""
    return render(request, 'pages/inventory_dashboard.html')

@login_required
def stock_movements(request):
    """تقرير حركات المخزون - Stock Movements Report"""
    return render(request, 'pages/stock_movements.html')

@login_required
def slow_moving_report(request):
    """تقرير القطع بطيئة الحركة - Slow Moving Items Report"""
    return render(request, 'pages/slow_moving_report.html')

@login_required
def low_stock_report(request):
    """تقرير القطع منخفضة المخزون - Low Stock Report"""
    return render(request, 'pages/low_stock_report.html')


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
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')

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

        from inventory.models import InventoryItem, StockMovement, WarehouseLocation
        from cars.models import Part

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
            default_location, _ = WarehouseLocation.objects.get_or_create(
                warehouse='مخزن التفكيك',
                defaults={'description': 'موقع افتراضي للقطع المفككة'}
            )

            # معالجة كل قطعة
            for part_data in parts:
                # الحصول على الفئة
                from cars.models import PartCategory
                category_name = part_data.get('category', 'MISC')

                # محاولة الحصول على الفئة أو إنشاء فئة افتراضية
                try:
                    category = PartCategory.objects.get(name=category_name)
                except PartCategory.DoesNotExist:
                    # إنشاء فئة "متنوعة" إذا لم تكن موجودة
                    category, _ = PartCategory.objects.get_or_create(
                        name='متنوعة',
                        defaults={'name_ar': 'متنوعة', 'description': 'قطع متنوعة'}
                    )

                # إنشاء أو الحصول على القطعة
                part_name_ar = part_data.get('name_ar', '')
                part_name_en = part_data.get('name_en', part_name_ar)

                part, created = Part.objects.get_or_create(
                    name_ar=part_name_ar,
                    category=category,
                    defaults={
                        'name': part_name_en,
                        'description': f"قطعة من {vehicle.make.name_ar} {vehicle.model.name_ar} {vehicle.year}"
                    }
                )

                # إنشاء عنصر في المخزون
                cost_price = part_data.get('cost_price')
                inventory_item = InventoryItem.objects.create(
                    part=part,
                    vehicle_source=vehicle,
                    condition=part_data.get('condition', 'USED_GOOD'),
                    quantity=1,
                    cost_price=Decimal(str(cost_price)) if cost_price else None,
                    selling_price=Decimal(str(part_data.get('price', 0))),
                    location=default_location,
                    status='AVAILABLE',
                    added_by=request.user
                )

                # إنشاء حركة مخزون
                StockMovement.objects.create(
                    item=inventory_item,
                    movement_type='IN',
                    quantity=1,
                    reference=f'DISMANTLE-{vehicle.id}',
                    reason=f'تفكيك سيارة: {vehicle.make.name_ar} {vehicle.model.name_ar} {vehicle.year}',
                    performed_by=request.user
                )
                
                created_items.append({
                    'id': inventory_item.id,
                    'sku': inventory_item.sku,
                    'part_name_ar': part.name_ar,
                    'part_name': part.name,
                    'cost_price': str(inventory_item.cost_price) if inventory_item.cost_price else None,
                    'selling_price': str(inventory_item.selling_price),
                    'condition': inventory_item.condition,
                    'condition_display': inventory_item.get_condition_display()
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
