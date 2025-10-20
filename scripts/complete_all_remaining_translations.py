#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete ALL remaining translations - Comprehensive dictionary
"""

import re

# Comprehensive EN to AR dictionary for all remaining translations
EN_TO_AR_COMPLETE = {
    # User & Authentication
    "last login": "آخر تسجيل دخول",
    
    # Car Make/Model fields
    "car make": "ماركة السيارة",
    "car makes": "ماركات السيارات",
    "production start year": "سنة بداية الإنتاج",
    "production end year": "سنة نهاية الإنتاج",
    "body type": "نوع الهيكل",
    "car model": "موديل السيارة",
    "car models": "موديلات السيارات",
    
    # Category fields
    "category name": "اسم الفئة",
    "parent category": "الفئة الأم",
    "icon class": "رمز الأيقونة",
    "sort order": "ترتيب العرض",
    "part category": "فئة القطعة",
    "part categories": "فئات القطع",
    
    # Part/Inventory fields
    "part number": "رقم القطعة",
    "compatible models": "الموديلات المتوافقة",
    "default image": "الصورة الافتراضية",
    "universal part": "قطعة عامة",
    "parts": "القطع",
    "Item Information": "معلومات الصنف",
    "Quantity": "الكمية",
    "Low Stock": "مخزون منخفض",
    "barcode": "الباركود",
    "minimum quantity": "الحد الأدنى للكمية",
    "added by": "أضيف بواسطة",
    "added at": "أضيف في",
    "inventory item": "صنف المخزون",
    "inventory items": "أصناف المخزون",
    "primary image": "الصورة الأساسية",
    "inventory item image": "صورة الصنف",
    "inventory item images": "صور الصنف",
    
    # Condition statuses
    "Excellent": "ممتاز",
    "Good": "جيد",
    "Fair": "مقبول",
    "Poor": "سيئ",
    "Salvage": "للإنقاذ",
    "Refurbished": "مجدد",
    
    # Vehicle fields
    "intake notes": "ملاحظات الاستلام",
    "received by": "مستلم بواسطة",
    "dismantled": "مفكك",
    "dismantled date": "تاريخ التفكيك",
    "vehicles": "السيارات",
    "source vehicle": "السيارة المصدر",
    "image": "الصورة",
    "caption": "التعليق",
    "primary photo": "الصورة الأساسية",
    "uploaded at": "رفع في",
    "vehicle photo": "صورة السيارة",
    "vehicle photos": "صور السيارة",
    
    # Customer fields
    "Address": "العنوان",
    "Financial": "المالية",
    "Additional": "إضافي",
    "Note": "ملاحظة",
    "Business": "تجاري",
    "business name": "اسم النشاط التجاري",
    "secondary phone": "هاتف ثانوي",
    "postal code": "الرمز البريدي",
    "tax ID": "الرقم الضريبي",
    "created by": "أنشئ بواسطة",
    "customers": "العملاء",
    "credit amount": "مبلغ الائتمان",
    "reason": "السبب",
    "reference": "المرجع",
    "issued by": "أصدر بواسطة",
    "issued at": "أصدر في",
    "used": "مستخدم",
    "used at": "استخدم في",
    "customer credit": "رصيد العميل",
    "customer credits": "أرصدة العملاء",
    "note": "ملاحظة",
    "important": "مهم",
    "customer note": "ملاحظة العميل",
    "customer notes": "ملاحظات العملاء",
    
    # Warehouse/Location fields
    "Transfer Information": "معلومات التحويل",
    "Status": "الحالة",
    "Tracking": "التتبع",
    "warehouse": "المستودع",
    "aisle": "الممر",
    "shelf": "الرف",
    "bin": "الصندوق",
    "warehouse locations": "مواقع المستودعات",
    "from location": "من الموقع",
    "to location": "إلى الموقع",
    
    # Stock statuses
    "Available": "متوفر",
    "Reserved": "محجوز",
    "Sold": "مباع",
    "Returned": "مرتجع",
    
    # Movement types
    "Stock In": "وارد",
    "Stock Out": "صادر",
    "Adjustment": "تعديل",
    "Transfer": "تحويل",
    "Return": "إرجاع",
    "movement type": "نوع الحركة",
    "performed by": "نفذ بواسطة",
    "performed at": "نفذ في",
    "stock movement": "حركة المخزون",
    "stock movements": "حركات المخزون",
    "Approved": "موافق عليه",
    "approved at": "وافق عليه في",
    
    # Sales fields
    "sale": "البيع",
    "sales": "المبيعات",
    "order": "الطلب",
    "orders": "الطلبات",
    "invoice": "الفاتورة",
    "invoices": "الفواتير",
    "payment": "الدفع",
    "payments": "المدفوعات",
    "discount": "الخصم",
    "total": "الإجمالي",
    "subtotal": "المجموع الفرعي",
    "tax": "الضريبة",
    "grand total": "الإجمالي الكلي",
    
    # Common fields
    "name": "الاسم",
    "description": "الوصف",
    "price": "السعر",
    "cost": "التكلفة",
    "quantity": "الكمية",
    "date": "التاريخ",
    "time": "الوقت",
    "created": "تاريخ الإنشاء",
    "updated": "تاريخ التحديث",
    "active": "نشط",
    "inactive": "غير نشط",
    "enabled": "مفعل",
    "disabled": "معطل",
    
    # Actions (if any left)
    "add": "إضافة",
    "edit": "تعديل",
    "delete": "حذف",
    "save": "حفظ",
    "cancel": "إلغاء",
    "search": "بحث",
    "filter": "تصفية",
    "export": "تصدير",
    "import": "استيراد",
    "print": "طباعة",
    "view": "عرض",
    "close": "إغلاق",
}

# AR to EN dictionary (less needed but included for completeness)
AR_TO_EN_COMPLETE = {
    # Reverse translations for any Arabic msgid with empty English msgstr
    "آخر تسجيل دخول": "Last Login",
    "ماركة السيارة": "Car Make",
    "ماركات السيارات": "Car Makes",
    "سنة بداية الإنتاج": "Production Start Year",
    "سنة نهاية الإنتاج": "Production End Year",
    "نوع الهيكل": "Body Type",
    "موديل السيارة": "Car Model",
    "موديلات السيارات": "Car Models",
    "اسم الفئة": "Category Name",
    "الفئة الأم": "Parent Category",
    "رمز الأيقونة": "Icon Class",
    "ترتيب العرض": "Sort Order",
    "فئة القطعة": "Part Category",
    "فئات القطع": "Part Categories",
    "رقم القطعة": "Part Number",
    "الموديلات المتوافقة": "Compatible Models",
    "الصورة الافتراضية": "Default Image",
    "قطعة عامة": "Universal Part",
    "القطع": "Parts",
    "معلومات الصنف": "Item Information",
    "الكمية": "Quantity",
    "مخزون منخفض": "Low Stock",
    "الباركود": "Barcode",
    "الحد الأدنى للكمية": "Minimum Quantity",
    "أضيف بواسطة": "Added By",
    "أضيف في": "Added At",
    "صنف المخزون": "Inventory Item",
    "أصناف المخزون": "Inventory Items",
    "الصورة الأساسية": "Primary Image",
    "صورة الصنف": "Inventory Item Image",
    "صور الصنف": "Inventory Item Images",
    "ممتاز": "Excellent",
    "جيد": "Good",
    "مقبول": "Fair",
    "سيئ": "Poor",
    "للإنقاذ": "Salvage",
    "مجدد": "Refurbished",
    "ملاحظات الاستلام": "Intake Notes",
    "مستلم بواسطة": "Received By",
    "مفكك": "Dismantled",
    "تاريخ التفكيك": "Dismantled Date",
    "السيارات": "Vehicles",
    "السيارة المصدر": "Source Vehicle",
    "الصورة": "Image",
    "التعليق": "Caption",
    "رفع في": "Uploaded At",
    "صورة السيارة": "Vehicle Photo",
    "صور السيارة": "Vehicle Photos",
    "العنوان": "Address",
    "المالية": "Financial",
    "إضافي": "Additional",
    "ملاحظة": "Note",
    "تجاري": "Business",
    "اسم النشاط التجاري": "Business Name",
    "هاتف ثانوي": "Secondary Phone",
    "الرمز البريدي": "Postal Code",
    "الرقم الضريبي": "Tax ID",
    "أنشئ بواسطة": "Created By",
    "العملاء": "Customers",
    "مبلغ الائتمان": "Credit Amount",
    "السبب": "Reason",
    "المرجع": "Reference",
    "أصدر بواسطة": "Issued By",
    "أصدر في": "Issued At",
    "مستخدم": "Used",
    "استخدم في": "Used At",
    "رصيد العميل": "Customer Credit",
    "أرصدة العملاء": "Customer Credits",
    "مهم": "Important",
    "ملاحظة العميل": "Customer Note",
    "ملاحظات العملاء": "Customer Notes",
    "معلومات التحويل": "Transfer Information",
    "الحالة": "Status",
    "التتبع": "Tracking",
    "المستودع": "Warehouse",
    "الممر": "Aisle",
    "الرف": "Shelf",
    "الصندوق": "Bin",
    "مواقع المستودعات": "Warehouse Locations",
    "من الموقع": "From Location",
    "إلى الموقع": "To Location",
    "متوفر": "Available",
    "محجوز": "Reserved",
    "مباع": "Sold",
    "مرتجع": "Returned",
    "وارد": "Stock In",
    "صادر": "Stock Out",
    "تعديل": "Adjustment",
    "تحويل": "Transfer",
    "إرجاع": "Return",
    "نوع الحركة": "Movement Type",
    "نفذ بواسطة": "Performed By",
    "نفذ في": "Performed At",
    "حركة المخزون": "Stock Movement",
    "حركات المخزون": "Stock Movements",
    "موافق عليه": "Approved",
    "وافق عليه في": "Approved At",
}


def translate_po_file(po_file_path, dictionary, language_name):
    """
    Translate empty msgstr using comprehensive dictionary
    """
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changes = 0
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Look for msgid lines
        if line.startswith('msgid "') and i + 1 < len(lines):
            # Extract msgid text
            msgid_match = re.match(r'msgid "(.*)"', line)
            if msgid_match:
                msgid_text = msgid_match.group(1)
                
                # Check if next line is empty msgstr
                if lines[i + 1].strip() == 'msgstr ""':
                    # Look up in dictionary
                    if msgid_text in dictionary:
                        translation = dictionary[msgid_text]
                        lines[i + 1] = f'msgstr "{translation}"\n'
                        changes += 1
                        print(f"  ✅ {msgid_text[:40]:40} → {translation[:40]}")
        
        i += 1
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return changes


def main():
    print("=" * 80)
    print("🌍 Completing ALL Remaining Translations - Final Pass")
    print("=" * 80)
    print()
    
    # Translate Arabic file (EN to AR)
    print("📝 Processing: locale/ar/LC_MESSAGES/django.po (English → Arabic)")
    ar_changes = translate_po_file('locale/ar/LC_MESSAGES/django.po', EN_TO_AR_COMPLETE, 'Arabic')
    print(f"\n  ✅ Translated {ar_changes} strings")
    print()
    
    # Translate English file (AR to EN)
    print("📝 Processing: locale/en/LC_MESSAGES/django.po (Arabic → English)")
    en_changes = translate_po_file('locale/en/LC_MESSAGES/django.po', AR_TO_EN_COMPLETE, 'English')
    print(f"\n  ✅ Translated {en_changes} strings")
    print()
    
    print("=" * 80)
    print(f"✅ Total: {ar_changes + en_changes} translations completed")
    print("=" * 80)
    print()
    print("🔄 Next step: Run 'python manage.py compilemessages'")


if __name__ == '__main__':
    main()
