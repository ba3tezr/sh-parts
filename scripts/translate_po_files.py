#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to automatically translate .po files
Translates English to Arabic and Arabic to English
"""

import re
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Translation dictionary - English to Arabic
EN_TO_AR = {
    # Admin
    "Personal info": "المعلومات الشخصية",
    "Permissions": "الصلاحيات",
    "Security": "الأمان",
    "Important dates": "التواريخ المهمة",
    
    # User fields
    "username": "اسم المستخدم",
    "email address": "البريد الإلكتروني",
    "first name": "الاسم الأول",
    "last name": "الاسم الأخير",
    "phone number": "رقم الهاتف",
    "role": "الدور الوظيفي",
    "staff status": "حالة الموظف",
    "active": "نشط",
    "date joined": "تاريخ الانضمام",
    
    # Roles
    "Administrator": "مدير النظام",
    "Manager": "مدير",
    "Sales": "المبيعات",
    "Warehouse": "المستودع",
    
    # Messages
    "The Username field must be set": "يجب تعيين حقل اسم المستخدم",
    "Superuser must have is_staff=True.": "يجب أن يكون المستخدم المتميز موظفاً",
    "Superuser must have is_superuser=True.": "يجب أن يكون المستخدم المتميز مديراً",
    
    # Car fields
    "make name": "اسم الماركة",
    "make name (Arabic)": "اسم الماركة (عربي)",
    "logo": "الشعار",
    "created at": "تاريخ الإنشاء",
    "updated at": "تاريخ التحديث",
    "model name": "اسم الموديل",
    "model name (Arabic)": "اسم الموديل (عربي)",
    "year": "السنة",
    "make": "الماركة",
    "part name": "اسم القطعة",
    "part name (Arabic)": "اسم القطعة (عربي)",
    "category": "الفئة",
    "description": "الوصف",
    "is active": "نشط",
    
    # Vehicle fields
    "VIN": "رقم الشاسيه",
    "model": "الموديل",
    "color": "اللون",
    "mileage": "عداد المسافات",
    "intake date": "تاريخ الاستلام",
    "purchase price": "سعر الشراء",
    "notes": "ملاحظات",
    "status": "الحالة",
    "dismantling started": "بدء التفكيك",
    "dismantling completed": "اكتمال التفكيك",
    "photos": "الصور",
    
    # Status choices
    "Pending": "قيد الانتظار",
    "In Progress": "قيد التنفيذ",
    "Completed": "مكتمل",
    "Cancelled": "ملغي",
    
    # Vehicle Admin
    "Vehicle Information": "معلومات السيارة",
    "Intake Details": "تفاصيل الاستلام",
    "Dismantling Status": "حالة التفكيك",
    "Timestamps": "الطوابع الزمنية",
    
    # Customer fields
    "customer code": "كود العميل",
    "customer type": "نوع العميل",
    "Individual": "فرد",
    "Company": "شركة",
    "phone": "الهاتف",
    "email": "البريد الإلكتروني",
    "address": "العنوان",
    "city": "المدينة",
    "country": "الدولة",
    "tax number": "الرقم الضريبي",
    "credit limit": "الحد الائتماني",
    "current balance": "الرصيد الحالي",
    
    # Customer Admin
    "Basic Information": "المعلومات الأساسية",
    "Contact Information": "معلومات الاتصال",
    "Financial Information": "المعلومات المالية",
    
    # Inventory fields
    "SKU": "رمز المنتج",
    "quantity": "الكمية",
    "cost price": "سعر التكلفة",
    "selling price": "سعر البيع",
    "location": "الموقع",
    "condition": "الحالة",
    "New": "جديد",
    "Used - Excellent": "مستعمل - ممتاز",
    "Used - Good": "مستعمل - جيد",
    "Used - Fair": "مستعمل - مقبول",
    "Damaged": "تالف",
    "vehicle": "السيارة",
    "part": "القطعة",
    "warehouse location": "موقع المستودع",
    "minimum stock": "الحد الأدنى للمخزون",
    "QR code": "رمز QR",
    
    # Inventory Admin
    "Part Information": "معلومات القطعة",
    "Stock Information": "معلومات المخزون",
    "Pricing": "التسعير",
    "Location & Tracking": "الموقع والتتبع",
    
    # Sales fields
    "invoice number": "رقم الفاتورة",
    "invoice date": "تاريخ الفاتورة",
    "customer": "العميل",
    "total amount": "المبلغ الإجمالي",
    "discount": "الخصم",
    "tax": "الضريبة",
    "final amount": "المبلغ النهائي",
    "payment status": "حالة الدفع",
    "Unpaid": "غير مدفوع",
    "Partial": "دفع جزئي",
    "Paid": "مدفوع",
    "payment method": "طريقة الدفع",
    "Cash": "نقدي",
    "Card": "بطاقة",
    "Bank Transfer": "تحويل بنكي",
    "paid amount": "المبلغ المدفوع",
    "remaining amount": "المبلغ المتبقي",
    
    # Sales Admin
    "Invoice Information": "معلومات الفاتورة",
    "Payment Information": "معلومات الدفع",
    
    # Sale Item fields
    "sale": "البيع",
    "item": "المنتج",
    "unit price": "سعر الوحدة",
    "subtotal": "المجموع الفرعي",
    
    # Navigation
    "Dashboard": "لوحة التحكم",
    "Vehicles": "السيارات",
    "Inventory": "المخزون",
    "Customers": "العملاء",
    "Reports": "التقارير",
    "System Management": "إدارة النظام",
    "Price Management": "إدارة الأسعار",
    "Logout": "تسجيل الخروج",
    
    # Common actions
    "Add": "إضافة",
    "Edit": "تعديل",
    "Delete": "حذف",
    "Save": "حفظ",
    "Cancel": "إلغاء",
    "Search": "بحث",
    "Filter": "تصفية",
    "Export": "تصدير",
    "Print": "طباعة",
    "View": "عرض",
    "Close": "إغلاق",
    "Confirm": "تأكيد",
    "Yes": "نعم",
    "No": "لا",
    "OK": "موافق",
    
    # Login page
    "تسجيل الدخول": "تسجيل الدخول",
    "نظام قطع غيار السيارات": "نظام قطع غيار السيارات",
    "SH Parts Management System": "نظام إدارة قطع غيار السيارات",
    "اسم المستخدم": "اسم المستخدم",
    "كلمة المرور": "كلمة المرور",
    "تذكرني": "تذكرني",
    "البيانات الافتراضية: admin / admin123": "البيانات الافتراضية: admin / admin123",
    "جميع الحقوق محفوظة": "جميع الحقوق محفوظة",
    "تطوير": "تطوير",
    
    # Messages
    "Loading...": "جاري التحميل...",
    "Success": "نجح",
    "Error": "خطأ",
    "Warning": "تحذير",
    "Info": "معلومات",
    "Are you sure?": "هل أنت متأكد؟",
    "This action cannot be undone": "لا يمكن التراجع عن هذا الإجراء",
    "No data available": "لا توجد بيانات",
    "Please select": "الرجاء الاختيار",
    "Required field": "حقل مطلوب",
    "Invalid input": "إدخال غير صحيح",

    # Additional fields
    "is active": "نشط",
    "Company": "شركة",
    "address": "العنوان",
    "tax number": "الرقم الضريبي",
    "current balance": "الرصيد الحالي",
    "Financial Information": "المعلومات المالية",
    "Part Information": "معلومات القطعة",
    "Stock Information": "معلومات المخزون",
    "minimum stock": "الحد الأدنى للمخزون",
    "Invoice Information": "معلومات الفاتورة",
    "Payment Information": "معلومات الدفع",
    "invoice date": "تاريخ الفاتورة",
    "discount": "الخصم",
    "tax": "الضريبة",
    "final amount": "المبلغ النهائي",
    "Partial": "دفع جزئي",
    "Paid": "مدفوع",
    "Card": "بطاقة",
    "remaining amount": "المبلغ المتبقي",
    "photos": "الصور",
    "dismantling started": "بدء التفكيك",
    "dismantling completed": "اكتمال التفكيك",
    "In Progress": "قيد التنفيذ",

    # More common terms
    "name": "الاسم",
    "code": "الكود",
    "type": "النوع",
    "date": "التاريخ",
    "time": "الوقت",
    "price": "السعر",
    "amount": "المبلغ",
    "total": "الإجمالي",
    "details": "التفاصيل",
    "information": "المعلومات",
    "list": "القائمة",
    "report": "التقرير",
    "settings": "الإعدادات",
    "profile": "الملف الشخصي",
    "user": "المستخدم",
    "users": "المستخدمون",
    "admin": "المدير",
    "management": "الإدارة",
    "system": "النظام",
    "home": "الرئيسية",
    "back": "رجوع",
    "next": "التالي",
    "previous": "السابق",
    "submit": "إرسال",
    "reset": "إعادة تعيين",
    "clear": "مسح",
    "refresh": "تحديث",
    "download": "تحميل",
    "upload": "رفع",
    "import": "استيراد",
    "select": "اختيار",
    "all": "الكل",
    "none": "لا شيء",
    "other": "أخرى",
    "actions": "الإجراءات",
    "options": "الخيارات",
    "help": "مساعدة",
    "about": "حول",
    "contact": "اتصل بنا",
    "language": "اللغة",
    "theme": "المظهر",
    "notification": "الإشعار",
    "notifications": "الإشعارات",
    "message": "الرسالة",
    "messages": "الرسائل",
    "alert": "تنبيه",
    "alerts": "التنبيهات",
    "today": "اليوم",
    "yesterday": "أمس",
    "tomorrow": "غداً",
    "week": "أسبوع",
    "month": "شهر",
    "year": "سنة",
    "from": "من",
    "to": "إلى",
    "between": "بين",
    "and": "و",
    "or": "أو",
    "not": "ليس",
    "with": "مع",
    "without": "بدون",
    "in": "في",
    "out": "خارج",
    "on": "على",
    "off": "إيقاف",
    "enabled": "مفعل",
    "disabled": "معطل",
    "available": "متاح",
    "unavailable": "غير متاح",
    "online": "متصل",
    "offline": "غير متصل",
    "public": "عام",
    "private": "خاص",
    "draft": "مسودة",
    "published": "منشور",
    "archived": "مؤرشف",
    "deleted": "محذوف",
    "created": "تم الإنشاء",
    "updated": "تم التحديث",
    "modified": "تم التعديل",
    "by": "بواسطة",
    "at": "في",
    "ago": "منذ",
    "just now": "الآن",
    "minutes": "دقائق",
    "hours": "ساعات",
    "days": "أيام",
    "weeks": "أسابيع",
    "months": "أشهر",
    "years": "سنوات",
}

# Arabic to English (reverse dictionary)
AR_TO_EN = {
    # Navigation
    "لوحة التحكم": "Dashboard",
    "السيارات": "Vehicles",
    "المخزون": "Inventory",
    "العملاء": "Customers",
    "التقارير": "Reports",
    "إدارة النظام": "System Management",
    "إدارة الأسعار": "Price Management",
    "تسجيل الخروج": "Logout",
    "الملف الشخصي": "Profile",
    "الإعدادات": "Settings",
    "لوحة الإدارة": "Admin Panel",
    
    # Login
    "تسجيل الدخول": "Login",
    "نظام قطع غيار السيارات": "Auto Parts Management System",
    "اسم المستخدم": "Username",
    "كلمة المرور": "Password",
    "تذكرني": "Remember me",
    "البيانات الافتراضية: admin / admin123": "Default credentials: admin / admin123",
    "جميع الحقوق محفوظة": "All rights reserved",
    "تطوير": "Developed by",
    
    # Common
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
    "تأكيد": "Confirm",
    "نعم": "Yes",
    "لا": "No",
    "موافق": "OK",
    
    # Status
    "نشط": "Active",
    "غير نشط": "Inactive",
    "قيد الانتظار": "Pending",
    "قيد التنفيذ": "In Progress",
    "مكتمل": "Completed",
    "ملغي": "Cancelled",
    
    # Messages
    "جاري التحميل...": "Loading...",
    "نجح": "Success",
    "خطأ": "Error",
    "تحذير": "Warning",
    "معلومات": "Information",
    "هل أنت متأكد؟": "Are you sure?",
    "لا توجد بيانات": "No data available",

    # More translations AR → EN
    "الاسم": "Name",
    "الكود": "Code",
    "النوع": "Type",
    "التاريخ": "Date",
    "الوقت": "Time",
    "السعر": "Price",
    "المبلغ": "Amount",
    "الإجمالي": "Total",
    "التفاصيل": "Details",
    "المعلومات": "Information",
    "القائمة": "List",
    "التقرير": "Report",
    "الإعدادات": "Settings",
    "الملف الشخصي": "Profile",
    "المستخدم": "User",
    "المستخدمون": "Users",
    "المدير": "Admin",
    "الإدارة": "Management",
    "النظام": "System",
    "الرئيسية": "Home",
    "رجوع": "Back",
    "التالي": "Next",
    "السابق": "Previous",
    "إرسال": "Submit",
    "إعادة تعيين": "Reset",
    "مسح": "Clear",
    "تحديث": "Refresh",
    "تحميل": "Download",
    "رفع": "Upload",
    "استيراد": "Import",
    "اختيار": "Select",
    "الكل": "All",
    "لا شيء": "None",
    "أخرى": "Other",
    "الإجراءات": "Actions",
    "الخيارات": "Options",
    "مساعدة": "Help",
    "حول": "About",
    "اتصل بنا": "Contact",
    "اللغة": "Language",
    "المظهر": "Theme",
    "الإشعار": "Notification",
    "الإشعارات": "Notifications",
    "الرسالة": "Message",
    "الرسائل": "Messages",
    "تنبيه": "Alert",
    "التنبيهات": "Alerts",
    "اليوم": "Today",
    "أمس": "Yesterday",
    "غداً": "Tomorrow",
    "أسبوع": "Week",
    "شهر": "Month",
    "سنة": "Year",
    "من": "From",
    "إلى": "To",
    "بين": "Between",
    "و": "And",
    "أو": "Or",
    "ليس": "Not",
    "مع": "With",
    "بدون": "Without",
    "في": "In",
    "خارج": "Out",
    "على": "On",
    "إيقاف": "Off",
    "مفعل": "Enabled",
    "معطل": "Disabled",
    "متاح": "Available",
    "غير متاح": "Unavailable",
    "متصل": "Online",
    "غير متصل": "Offline",
    "عام": "Public",
    "خاص": "Private",
    "مسودة": "Draft",
    "منشور": "Published",
    "مؤرشف": "Archived",
    "محذوف": "Deleted",
    "تم الإنشاء": "Created",
    "تم التحديث": "Updated",
    "تم التعديل": "Modified",
    "بواسطة": "By",
    "منذ": "Ago",
    "الآن": "Just now",
    "دقائق": "Minutes",
    "ساعات": "Hours",
    "أيام": "Days",
    "أسابيع": "Weeks",
    "أشهر": "Months",
    "سنوات": "Years",

    # Additional specific translations
    "المعلومات الأساسية": "Basic Information",
    "معلومات الاتصال": "Contact Information",
    "المعلومات المالية": "Financial Information",
    "معلومات السيارة": "Vehicle Information",
    "تفاصيل الاستلام": "Intake Details",
    "حالة التفكيك": "Dismantling Status",
    "الطوابع الزمنية": "Timestamps",
    "معلومات القطعة": "Part Information",
    "معلومات المخزون": "Stock Information",
    "التسعير": "Pricing",
    "الموقع والتتبع": "Location & Tracking",
    "معلومات الفاتورة": "Invoice Information",
    "معلومات الدفع": "Payment Information",

    # Field names
    "اسم الماركة": "Make name",
    "اسم الموديل": "Model name",
    "اسم القطعة": "Part name",
    "رقم الشاسيه": "VIN",
    "الماركة": "Make",
    "الموديل": "Model",
    "السنة": "Year",
    "اللون": "Color",
    "عداد المسافات": "Mileage",
    "الحالة": "Condition",
    "تاريخ الاستلام": "Intake date",
    "سعر الشراء": "Purchase price",
    "السيارة": "Vehicle",
    "القطعة": "Part",
    "الفئة": "Category",
    "الوصف": "Description",
    "كود العميل": "Customer code",
    "نوع العميل": "Customer type",
    "البريد الإلكتروني": "Email",
    "الهاتف": "Phone",
    "العنوان": "Address",
    "المدينة": "City",
    "الدولة": "Country",
    "الرقم الضريبي": "Tax number",
    "الحد الائتماني": "Credit limit",
    "الرصيد الحالي": "Current balance",
    "ملاحظات": "Notes",
    "العميل": "Customer",
    "رمز المنتج": "SKU",
    "الكمية": "Quantity",
    "الموقع": "Location",
    "سعر التكلفة": "Cost price",
    "سعر البيع": "Selling price",
    "موقع المستودع": "Warehouse location",
    "الحد الأدنى للمخزون": "Minimum stock",
    "رمز QR": "QR code",
    "المنتج": "Item",
    "رقم الفاتورة": "Invoice number",
    "تاريخ الفاتورة": "Invoice date",
    "المبلغ الإجمالي": "Total amount",
    "الخصم": "Discount",
    "الضريبة": "Tax",
    "المبلغ النهائي": "Final amount",
    "حالة الدفع": "Payment status",
    "طريقة الدفع": "Payment method",
    "المبلغ المدفوع": "Paid amount",
    "المبلغ المتبقي": "Remaining amount",
    "البيع": "Sale",
    "سعر الوحدة": "Unit price",
    "المجموع الفرعي": "Subtotal",
    "الصور": "Photos",
    "بدء التفكيك": "Dismantling started",
    "اكتمال التفكيك": "Dismantling completed",

    # Status values
    "فرد": "Individual",
    "شركة": "Company",
    "جديد": "New",
    "مستعمل - ممتاز": "Used - Excellent",
    "مستعمل - جيد": "Used - Good",
    "مستعمل - مقبول": "Used - Fair",
    "تالف": "Damaged",
    "قيد الانتظار": "Pending",
    "قيد التنفيذ": "In Progress",
    "مكتمل": "Completed",
    "ملغي": "Cancelled",
    "غير مدفوع": "Unpaid",
    "دفع جزئي": "Partial",
    "مدفوع": "Paid",
    "نقدي": "Cash",
    "بطاقة": "Card",
    "تحويل بنكي": "Bank Transfer",

    # Roles
    "مدير النظام": "Administrator",
    "مدير": "Manager",
    "المبيعات": "Sales",
    "المستودع": "Warehouse",

    # User fields
    "اسم المستخدم": "Username",
    "كلمة المرور": "Password",
    "الاسم الأول": "First name",
    "الاسم الأخير": "Last name",
    "رقم الهاتف": "Phone number",
    "الدور الوظيفي": "Role",
    "حالة الموظف": "Staff status",
    "نشط": "Active",
    "تاريخ الانضمام": "Date joined",
    "تاريخ الإنشاء": "Created at",
    "تاريخ التحديث": "Updated at",
    "الشعار": "Logo",

    # System
    "المعلومات الشخصية": "Personal info",
    "الصلاحيات": "Permissions",
    "الأمان": "Security",
    "التواريخ المهمة": "Important dates",
}


def translate_po_file(po_file_path, translation_dict):
    """
    Translate empty msgstr in .po file using translation dictionary
    """
    print(f"\n📝 Processing: {po_file_path}")
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    translated_count = 0
    total_empty = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Find msgid lines
        if line.startswith('msgid "') and not line.startswith('msgid ""'):
            # Extract msgid text
            msgid_match = re.match(r'msgid "(.*)"', line)
            if msgid_match:
                msgid_text = msgid_match.group(1)
                
                # Check if next line is empty msgstr
                if i + 1 < len(lines) and lines[i + 1] == 'msgstr ""':
                    total_empty += 1
                    
                    # Try to find translation
                    if msgid_text in translation_dict:
                        translation = translation_dict[msgid_text]
                        lines[i + 1] = f'msgstr "{translation}"'
                        translated_count += 1
                        print(f"  ✅ {msgid_text} → {translation}")
        
        i += 1
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"\n📊 Summary for {os.path.basename(po_file_path)}:")
    print(f"  - Total empty msgstr: {total_empty}")
    print(f"  - Translated: {translated_count}")
    print(f"  - Remaining: {total_empty - translated_count}")
    
    return translated_count, total_empty


def main():
    """Main function"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Translate Arabic .po file (English to Arabic)
    ar_po = os.path.join(base_dir, 'locale', 'ar', 'LC_MESSAGES', 'django.po')
    if os.path.exists(ar_po):
        print("\n" + "="*60)
        print("🇸🇦 Translating Arabic .po file (EN → AR)")
        print("="*60)
        ar_translated, ar_total = translate_po_file(ar_po, EN_TO_AR)
    
    # Translate English .po file (Arabic to English)
    en_po = os.path.join(base_dir, 'locale', 'en', 'LC_MESSAGES', 'django.po')
    if os.path.exists(en_po):
        print("\n" + "="*60)
        print("🇬🇧 Translating English .po file (AR → EN)")
        print("="*60)
        en_translated, en_total = translate_po_file(en_po, AR_TO_EN)
    
    print("\n" + "="*60)
    print("✅ Translation Complete!")
    print("="*60)
    print(f"\n📊 Final Summary:")
    print(f"  Arabic: {ar_translated}/{ar_total} translated")
    print(f"  English: {en_translated}/{en_total} translated")
    print(f"\n⚠️  Note: Remaining untranslated strings need manual translation")
    print(f"\n🔄 Next step: Run 'python manage.py compilemessages' to compile translations")


if __name__ == '__main__':
    main()

