from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, Count
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
