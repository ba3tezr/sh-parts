#!/usr/bin/env python
"""اختبار شامل لجميع أجزاء النظام"""

import os
import django
import sys

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sh_parts.settings')
django.setup()

from django.contrib.auth import get_user_model
from cars.models import CarMake, CarModel, Part, Vehicle
from inventory.models import InventoryItem, WarehouseLocation
from customers.models import Customer
from sales.models import Sale
from django.db import connection

User = get_user_model()

def test_database():
    """اختبار قاعدة البيانات"""
    print("\n" + "="*50)
    print("🔍 اختبار قاعدة البيانات")
    print("="*50)
    
    tests = {
        'المستخدمين': User.objects.count(),
        'الماركات': CarMake.objects.count(),
        'الموديلات': CarModel.objects.count(),
        'القطع': Part.objects.count(),
        'السيارات': Vehicle.objects.count(),
        'المخزون': InventoryItem.objects.count(),
        'المواقع': WarehouseLocation.objects.count(),
        'العملاء': Customer.objects.count(),
        'المبيعات': Sale.objects.count(),
    }
    
    for name, count in tests.items():
        status = "✅" if count > 0 else "⚠️"
        print(f"{status} {name}: {count}")
    
    return all(count > 0 for name, count in tests.items() if name in ['المستخدمين', 'الماركات'])

def test_models():
    """اختبار نماذج البيانات"""
    print("\n" + "="*50)
    print("🔍 اختبار النماذج")
    print("="*50)
    
    errors = []
    
    # فحص Sale model
    try:
        from sales.models import Sale
        fields = [f.name for f in Sale._meta.fields]
        print(f"✅ Sale fields: {', '.join(fields[:5])}...")
        if 'created_at' not in fields:
            errors.append("Sale يفتقد حقل created_at")
    except Exception as e:
        errors.append(f"خطأ في Sale: {e}")
    
    # فحص Customer model
    try:
        from customers.models import Customer
        fields = [f.name for f in Customer._meta.fields]
        print(f"✅ Customer fields: {', '.join(fields[:5])}...")
    except Exception as e:
        errors.append(f"خطأ في Customer: {e}")
    
    # فحص InventoryItem model
    try:
        from inventory.models import InventoryItem
        fields = [f.name for f in InventoryItem._meta.fields]
        print(f"✅ InventoryItem fields: {', '.join(fields[:5])}...")
        if 'added_at' not in fields:
            errors.append("InventoryItem يفتقد حقل added_at")
    except Exception as e:
        errors.append(f"خطأ في InventoryItem: {e}")
    
    if errors:
        print("\n❌ أخطاء في النماذج:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    print("\n✅ جميع النماذج صحيحة")
    return True

def test_views():
    """اختبار الـ Views"""
    print("\n" + "="*50)
    print("🔍 اختبار Views")
    print("="*50)
    
    from django.urls import reverse
    from django.test import Client
    
    client = Client()
    
    # تسجيل الدخول
    user = User.objects.filter(is_superuser=True).first()
    if user:
        client.force_login(user)
        print(f"✅ تم تسجيل الدخول بـ: {user.email}")
    else:
        print("⚠️ لا يوجد مستخدم admin")
        return False
    
    views_to_test = {
        'dashboard': '/',
        'vehicles': '/vehicles/',
        'inventory': '/inventory/',
        'sales': '/sales/',
        'customers': '/customers/',
        'reports': '/reports/',
    }
    
    results = {}
    for name, url in views_to_test.items():
        try:
            response = client.get(url)
            status = "✅" if response.status_code == 200 else f"❌ ({response.status_code})"
            print(f"{status} {name}: {url}")
            results[name] = response.status_code == 200
        except Exception as e:
            print(f"❌ {name}: {e}")
            results[name] = False
    
    return all(results.values())

def test_api():
    """اختبار API"""
    print("\n" + "="*50)
    print("🔍 اختبار API")
    print("="*50)
    
    from django.test import Client
    
    client = Client()
    
    api_endpoints = {
        'settings': '/api/settings/',
        'makes': '/api/cars/makes/',
        'models': '/api/cars/models/',
        'parts': '/api/cars/parts/',
        'vehicles': '/api/cars/vehicles/',
        'inventory': '/api/inventory/items/',
        'customers': '/api/customers/',
        'sales': '/api/sales/',
    }
    
    results = {}
    for name, url in api_endpoints.items():
        try:
            response = client.get(url)
            status = "✅" if response.status_code in [200, 401] else f"❌ ({response.status_code})"
            print(f"{status} {name}: {url}")
            results[name] = response.status_code in [200, 401]
        except Exception as e:
            print(f"❌ {name}: {e}")
            results[name] = False
    
    return all(results.values())

def main():
    """تشغيل جميع الاختبارات"""
    print("\n" + "="*60)
    print("🚀 اختبار شامل لنظام SH Parts")
    print("="*60)
    
    results = {
        'قاعدة البيانات': test_database(),
        'النماذج': test_models(),
        'Views': test_views(),
        'API': test_api(),
    }
    
    print("\n" + "="*60)
    print("📊 ملخص الاختبارات")
    print("="*60)
    
    for name, passed in results.items():
        status = "✅ نجح" if passed else "❌ فشل"
        print(f"{status} - {name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ جميع الاختبارات نجحت!")
    else:
        print("❌ بعض الاختبارات فشلت - يرجى مراجعة الأخطاء أعلاه")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
