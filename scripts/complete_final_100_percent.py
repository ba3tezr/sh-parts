#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete 100% translation - Final comprehensive pass
"""

import re
import json

# COMPLETE dictionary for ALL remaining translations
COMPLETE_EN_DICT = {
    # Already done but ensuring consistency
    "اسم المستخدم": "Username",
    "كلمة المرور": "Password",
    "تسجيل الدخول": "Login",
    "تذكرني": "Remember Me",
    "جميع الحقوق محفوظة": "All Rights Reserved",
    "تطوير": "Developed by",
    
    # Dashboard
    "لوحة التحكم": "Dashboard",
    "إجمالي المبيعات": "Total Sales",
    "إجمالي المخزون": "Total Inventory",
    "إجمالي العملاء": "Total Customers",
    "الطلبات المعلقة": "Pending Orders",
    "آخر المبيعات": "Recent Sales",
    "عرض الكل": "View All",
    "رقم الفاتورة": "Invoice Number",
    "اسم العميل": "Customer Name",
    "الإجمالي": "Total",
    "الحالة": "Status",
    "التاريخ": "Date",
    "قطعة": "Part",
    "عميل": "Customer",
    "طلب": "Order",
    
    # Customers
    "العملاء": "Customers",
    "إضافة عميل": "Add Customer",
    "اسم العميل": "Customer Name",
    "رقم الهاتف": "Phone Number",
    "البريد الإلكتروني": "Email",
    "العنوان": "Address",
    "الرصيد": "Balance",
    "حذف": "Delete",
    "تعديل": "Edit",
    "عرض": "View",
    
    # Barcode
    "نظام الباركود": "Barcode System",
    "مسح الباركود": "Scan Barcode",
    "إدخال يدوي": "Manual Entry",
    "بدء المسح": "Start Scanning",
    "إيقاف المسح": "Stop Scanning",
    "طباعة": "Print",
    
    # Inventory
    "المخزون": "Inventory",
    "إضافة قطعة": "Add Part",
    "رقم القطعة": "Part Number",
    "اسم القطعة": "Part Name",
    "الكمية": "Quantity",
    "السعر": "Price",
    "الفئة": "Category",
    
    # Common
    "بحث": "Search",
    "تصدير": "Export",
    "استيراد": "Import",
    "حفظ": "Save",
    "إلغاء": "Cancel",
    "إغلاق": "Close",
    "تأكيد": "Confirm",
    "نعم": "Yes",
    "لا": "No",
    "موافق": "OK",
    "خطأ": "Error",
    "نجاح": "Success",
    "تحذير": "Warning",
    "معلومات": "Information",
    
    # Status
    "نشط": "Active",
    "غير نشط": "Inactive",
    "مكتمل": "Completed",
    "معلق": "Pending",
    "ملغي": "Cancelled",
    
    # Actions
    "إضافة": "Add",
    "تعديل": "Edit",
    "حذف": "Delete",
    "حفظ": "Save",
    "إلغاء": "Cancel",
    "بحث": "Search",
    "تصفية": "Filter",
    "تصدير": "Export",
    "طباعة": "Print",
    "عرض": "View",
    "إغلاق": "Close",
    "رجوع": "Back",
    
    # Messages
    "جاري التحميل...": "Loading...",
    "لا توجد بيانات": "No data available",
    "فشل تحميل البيانات": "Failed to load data",
    "تم الحفظ بنجاح": "Saved successfully",
    "تم الحذف بنجاح": "Deleted successfully",
    "حدث خطأ": "An error occurred",
    "هل أنت متأكد؟": "Are you sure?",
    "لا يمكن التراجع عن هذا الإجراء": "This action cannot be undone",
    
    # Units
    "قطعة": "Part",
    "قطع": "Parts",
    "عميل": "Customer",
    "عملاء": "Customers",
    "طلب": "Order",
    "طلبات": "Orders",
    "فاتورة": "Invoice",
    "فواتير": "Invoices",
    
    # Remaining specific terms
    "البيانات الافتراضية: admin / admin123": "Default credentials: admin / admin123",
    "نظام قطع غيار السيارات": "Car Parts System",
    "نظام إدارة SH Parts": "SH Parts Management System",
    "Zakee Tahawi": "Zakee Tahawi",
    "العربية": "Arabic",
    "English": "English",
}

COMPLETE_AR_DICT = {
    # Reverse - English to Arabic (less common but for completeness)
    "Username": "اسم المستخدم",
    "Password": "كلمة المرور",
    "Login": "تسجيل الدخول",
    "Dashboard": "لوحة التحكم",
    "Customers": "العملاء",
    "Inventory": "المخزون",
    "Sales": "المبيعات",
    "Reports": "التقارير",
    "Settings": "الإعدادات",
    "Logout": "تسجيل الخروج",
}


def complete_translations(po_file_path, dictionary, language_name):
    """
    Complete all remaining translations
    """
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changes = 0
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('msgid "') and i + 1 < len(lines):
            msgid_match = re.match(r'msgid "(.*)"', line)
            if msgid_match:
                msgid_text = msgid_match.group(1)
                
                # Check if next line is msgstr
                if lines[i + 1].startswith('msgstr "'):
                    msgstr_match = re.match(r'msgstr "(.*)"', lines[i + 1])
                    if msgstr_match:
                        current_msgstr = msgstr_match.group(1)
                        
                        # If msgid is in dictionary
                        if msgid_text in dictionary:
                            correct_msgstr = dictionary[msgid_text]
                            
                            # Update if empty or different
                            if current_msgstr == "" or current_msgstr != correct_msgstr:
                                lines[i + 1] = f'msgstr "{correct_msgstr}"\n'
                                changes += 1
                                status = "EMPTY" if current_msgstr == "" else f"WRONG: {current_msgstr[:20]}"
                                print(f"  ✅ {msgid_text[:30]:30} | {status:25} → {correct_msgstr[:30]}")
        
        i += 1
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return changes


def main():
    print("=" * 100)
    print("🎯 FINAL 100% Translation Completion - Ultimate Pass")
    print("=" * 100)
    print()
    
    # Complete English translations
    print("📝 Processing: locale/en/LC_MESSAGES/django.po (Arabic → English)")
    print("-" * 100)
    en_changes = complete_translations('locale/en/LC_MESSAGES/django.po', COMPLETE_EN_DICT, 'English')
    print(f"\n  ✅ Completed/Fixed {en_changes} translations")
    print()
    
    # Complete Arabic translations
    print("📝 Processing: locale/ar/LC_MESSAGES/django.po (English → Arabic)")
    print("-" * 100)
    ar_changes = complete_translations('locale/ar/LC_MESSAGES/django.po', COMPLETE_AR_DICT, 'Arabic')
    print(f"\n  ✅ Completed/Fixed {ar_changes} translations")
    print()
    
    print("=" * 100)
    print(f"✅ GRAND TOTAL: {ar_changes + en_changes} translations completed/fixed")
    print("=" * 100)
    print()
    print("🔄 Next steps:")
    print("  1. python manage.py compilemessages")
    print("  2. Restart Django server")
    print("  3. Test all pages in both languages!")
    print()


if __name__ == '__main__':
    main()
