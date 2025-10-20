#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete Arabic to English translation for django.po
"""

import re
import os

# Comprehensive Arabic to English dictionary
AR_TO_EN_COMPLETE = {
    # System & Navigation
    "نظام قطع غيار السيارات": "Auto Parts Management System",
    "نظام إدارة SH Parts": "SH Parts Management System",
    "لوحة التحكم": "Dashboard",
    "العربية": "Arabic",
    "Zakee Tahawi": "Zakee Tahawi",  # Name stays the same
    "لوحة الإدارة": "Admin Panel",
    "الملف الشخصي": "Profile",
    "الإعدادات": "Settings",
    "تسجيل الخروج": "Logout",
    "الرئيسية": "Home",
    "العملاء": "Customers",
    "المخزون": "Inventory",
    "السيارات": "Vehicles",
    "المبيعات": "Sales",
    "التقارير": "Reports",
    "إدارة النظام": "System Management",
    "إدارة الأسعار": "Price Management",
    
    # Login & Auth
    "تسجيل الدخول": "Login",
    "اسم المستخدم": "Username",
    "كلمة المرور": "Password",
    "تذكرني": "Remember me",
    "البيانات الافتراضية: admin / admin123": "Default credentials: admin / admin123",
    "جميع الحقوق محفوظة": "All rights reserved",
    "تطوير": "Developed by",
    
    # Common Actions
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
    
    # Customer Related
    "تفاصيل العميل": "Customer Details",
    "بيع جديد": "New Sale",
    "المعلومات الأساسية": "Basic Information",
    "تاريخ التسجيل": "Registration Date",
    "معلومات الاتصال": "Contact Information",
    "الهاتف": "Phone",
    "هاتف ثانوي": "Secondary Phone",
    "البريد الإلكتروني": "Email",
    "العنوان": "Address",
    "عرض على الخريطة": "View on Map",
    "الملخص المالي": "Financial Summary",
    "الرصيد المستحق": "Outstanding Balance",
    "حد الائتمان": "Credit Limit",
    "الائتمان المتاح": "Available Credit",
    "سجل المشتريات": "Purchase History",
    "المدفوعات": "Payments",
    "الأرصدة": "Balances",
    "الملاحظات": "Notes",
    "التحليلات": "Analytics",
    "سجل المدفوعات": "Payment History",
    "رقم الدفعة": "Payment Number",
    "الفاتورة": "Invoice",
    "الطريقة": "Method",
    "الأرصدة والمكافآت": "Balances & Rewards",
    "السبب": "Reason",
    "معدل الشراء": "Purchase Rate",
    "القطع المفضلة": "Favorite Parts",
    "الملاحظة": "Note",
    "ملاحظة مهمة": "Important Note",
    "المرجع": "Reference",
    "معرف العميل غير موجود": "Customer ID not found",
    "خطأ في تحميل بيانات العميل": "Error loading customer data",
    "لا توجد مشتريات": "No purchases",
    
    # Invoice & Sales
    "رقم الفاتورة": "Invoice Number",
    "التاريخ": "Date",
    "المبلغ": "Amount",
    "المدفوع": "Paid",
    "الحالة": "Status",
    "التفاصيل": "Details",
    "الإجمالي": "Total",
    "الخصم": "Discount",
    "الضريبة": "Tax",
    "المبلغ النهائي": "Final Amount",
    "المبلغ الإجمالي": "Total Amount",
    "المبلغ المدفوع": "Paid Amount",
    "المبلغ المتبقي": "Remaining Amount",
    "حالة الدفع": "Payment Status",
    "طريقة الدفع": "Payment Method",
    "المجموع الفرعي": "Subtotal",
    "سعر الوحدة": "Unit Price",
    
    # Inventory
    "المخزون": "Inventory",
    "القطعة": "Part",
    "الكمية": "Quantity",
    "السعر": "Price",
    "سعر التكلفة": "Cost Price",
    "سعر البيع": "Selling Price",
    "الموقع": "Location",
    "موقع المستودع": "Warehouse Location",
    "الحد الأدنى للمخزون": "Minimum Stock",
    "رمز المنتج": "SKU",
    "رمز QR": "QR Code",
    "المنتج": "Item",
    "الفئة": "Category",
    "الوصف": "Description",
    
    # Vehicle
    "السيارة": "Vehicle",
    "الماركة": "Make",
    "الموديل": "Model",
    "السنة": "Year",
    "اللون": "Color",
    "رقم الشاسيه": "VIN",
    "عداد المسافات": "Mileage",
    "تاريخ الاستلام": "Intake Date",
    "سعر الشراء": "Purchase Price",
    "الصور": "Photos",
    "بدء التفكيك": "Dismantling Started",
    "اكتمال التفكيك": "Dismantling Completed",
    "معلومات السيارة": "Vehicle Information",
    "تفاصيل الاستلام": "Intake Details",
    "حالة التفكيك": "Dismantling Status",
    
    # Status & Conditions
    "نشط": "Active",
    "غير نشط": "Inactive",
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
    "جديد": "New",
    "مستعمل - ممتاز": "Used - Excellent",
    "مستعمل - جيد": "Used - Good",
    "مستعمل - مقبول": "Used - Fair",
    "تالف": "Damaged",
    "فرد": "Individual",
    "شركة": "Company",
    
    # Messages
    "جاري التحميل...": "Loading...",
    "تم الحفظ بنجاح": "Saved successfully",
    "حدث خطأ": "An error occurred",
    "هل أنت متأكد؟": "Are you sure?",
    "تم الحذف بنجاح": "Deleted successfully",
    "فشل الحذف": "Failed to delete",
    "تم التحديث بنجاح": "Updated successfully",
    "فشل التحديث": "Failed to update",
    "تم الإضافة بنجاح": "Added successfully",
    "فشل الإضافة": "Failed to add",
    "لا توجد بيانات": "No data available",
    "الرجاء الانتظار": "Please wait",
    "تم النسخ": "Copied",
    "فشل النسخ": "Copy failed",
    "تم حفظ الملاحظة بنجاح": "Note saved successfully",
    "خطأ في حفظ الملاحظة": "Error saving note",
    "تم إضافة الرصيد بنجاح": "Balance added successfully",
    "خطأ في إضافة الرصيد": "Error adding balance",
    
    # Fields
    "الاسم": "Name",
    "الكود": "Code",
    "النوع": "Type",
    "الوقت": "Time",
    "ملاحظات": "Notes",
    "كود العميل": "Customer Code",
    "نوع العميل": "Customer Type",
    "المدينة": "City",
    "الدولة": "Country",
    "الرقم الضريبي": "Tax Number",
    "الحد الائتماني": "Credit Limit",
    "الرصيد الحالي": "Current Balance",
    "العميل": "Customer",
    "البيع": "Sale",
    
    # Common Terms
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
    
    # Additional
    "المعلومات": "Information",
    "القائمة": "List",
    "التقرير": "Report",
    "المستخدم": "User",
    "المستخدمون": "Users",
    "المدير": "Admin",
    "الإدارة": "Management",
    "النظام": "System",
    "الطوابع الزمنية": "Timestamps",
    "معلومات القطعة": "Part Information",
    "معلومات المخزون": "Stock Information",
    "التسعير": "Pricing",
    "الموقع والتتبع": "Location & Tracking",
    "معلومات الفاتورة": "Invoice Information",
    "معلومات الدفع": "Payment Information",
    "المعلومات المالية": "Financial Information",

    # More Customer Related
    "أضيف بواسطة": "Added by",
    "البائع": "Seller",
    "المتبقي": "Remaining",
    "عملاء نشطون": "Active Customers",
    "جدد هذا الشهر": "New This Month",
    "عملاء أفراد": "Individual Customers",
    "عملاء شركات": "Company Customers",
    "تحليل RFM": "RFM Analysis",
    "أفراد": "Individuals",
    "شركات": "Companies",
    "الحداثة (أيام)": "Recency (Days)",
    "عملاء جدد (شهر)": "New Customers (Month)",
    "عملاء معرضون للخطر": "At-Risk Customers",
    "لا شراء 90+ يوم": "No Purchase 90+ Days",
    "بحث (كود، اسم، هاتف، بريد)": "Search (Code, Name, Phone, Email)",
    "الأحدث": "Newest",
    "الأقدم": "Oldest",
    "الاسم (أ-ي)": "Name (A-Z)",
    "الاسم (ي-أ)": "Name (Z-A)",
    "الكود (تصاعدي)": "Code (Ascending)",
    "الكود (تنازلي)": "Code (Descending)",
    "بطاقات": "Cards",
    "جدول": "Table",
    "البريد": "Email",
    "عملية": "Operation",
    "حدث خطأ أثناء حفظ العميل": "Error occurred while saving customer",
    "العودة": "Return",
    "الحداثة": "Recency",
    "التكرار": "Frequency",
    "ديون 90+ يوم": "Debts 90+ Days",

    # Dashboard & Stats
    "إجمالي المبيعات": "Total Sales",
    "إجمالي المخزون": "Total Inventory",
    "إجمالي العملاء": "Total Customers",
    "قطعة": "Piece",
    "عميل": "Customer",
    "المبيعات الشهرية": "Monthly Sales",
    "أفضل المنتجات": "Top Products",
    "آخر الطلبات": "Recent Orders",
    "التنبيهات": "Alerts",
    "مخزون منخفض": "Low Stock",
    "طلبات معلقة": "Pending Orders",

    # Orders & Sales
    "الطلبات": "Orders",
    "طلب جديد": "New Order",
    "قائمة الطلبات": "Orders List",
    "رقم الطلب": "Order Number",
    "نوع السيارة": "Vehicle Type",
    "حالة الطلب": "Order Status",
    "تفاصيل الطلب": "Order Details",
    "إضافة منتج": "Add Product",
    "المنتجات": "Products",
    "الكمية المتاحة": "Available Quantity",
    "إجمالي الطلب": "Order Total",

    # Inventory & Parts
    "إضافة قطعة": "Add Part",
    "تعديل قطعة": "Edit Part",
    "حذف قطعة": "Delete Part",
    "اسم القطعة": "Part Name",
    "رقم القطعة": "Part Number",
    "الكمية المتوفرة": "Available Quantity",
    "الكمية المحجوزة": "Reserved Quantity",
    "نقطة إعادة الطلب": "Reorder Point",
    "المورد": "Supplier",
    "تاريخ الإضافة": "Date Added",
    "آخر تحديث": "Last Update",

    # Reports
    "تقرير المبيعات": "Sales Report",
    "تقرير المخزون": "Inventory Report",
    "تقرير العملاء": "Customers Report",
    "تقرير الأرباح": "Profit Report",
    "من تاريخ": "From Date",
    "إلى تاريخ": "To Date",
    "عرض التقرير": "View Report",
    "تصدير PDF": "Export PDF",
    "تصدير Excel": "Export Excel",

    # Settings
    "الإعدادات العامة": "General Settings",
    "إعدادات النظام": "System Settings",
    "إعدادات الطباعة": "Print Settings",
    "إعدادات الإشعارات": "Notification Settings",
    "تغيير كلمة المرور": "Change Password",
    "كلمة المرور الحالية": "Current Password",
    "كلمة المرور الجديدة": "New Password",
    "تأكيد كلمة المرور": "Confirm Password",

    # Validation & Errors
    "هذا الحقل مطلوب": "This field is required",
    "البريد الإلكتروني غير صحيح": "Invalid email",
    "رقم الهاتف غير صحيح": "Invalid phone number",
    "الرجاء إدخال قيمة صحيحة": "Please enter a valid value",
    "الرجاء اختيار عنصر": "Please select an item",
    "تم الحفظ بنجاح": "Saved successfully",
    "فشل الحفظ": "Save failed",
    "تم الحذف بنجاح": "Deleted successfully",
    "فشل الحذف": "Delete failed",
    "الرجاء ملء جميع الحقول المطلوبة": "Please fill all required fields",
    "هل أنت متأكد من حذف هذه السيارة؟ لا يمكن التراجع عن هذا الإجراء.": "Are you sure you want to delete this vehicle? This action cannot be undone.",

    # Final Missing Terms
    "الحد الأدنى": "Minimum",
    "الأولوية": "Priority",
    "30-60 يوم": "30-60 Days",
    "60-90 يوم": "60-90 Days",
    "90-180 يوم": "90-180 Days",
    "+180 يوم": "+180 Days",
    "الفلاتر": "Filters",
    "وارد": "Incoming",
    "صادر": "Outgoing",
    "إرجاع": "Return",
    "تحويل": "Transfer",
    "SKU, قطعة, مستخدم...": "SKU, Part, User...",
}


def translate_po_file(po_file_path):
    """Translate Arabic msgid to English msgstr in .po file"""
    print(f"\n📝 Processing: {po_file_path}")
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    translated_count = 0
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Find msgid with Arabic text
        if line.startswith('msgid "') and not line.startswith('msgid ""'):
            msgid_match = re.match(r'msgid "(.*)"', line)
            if msgid_match:
                msgid_text = msgid_match.group(1)
                
                # Check if next line is empty msgstr
                if i + 1 < len(lines) and lines[i + 1].strip() == 'msgstr ""':
                    # Try to find translation
                    if msgid_text in AR_TO_EN_COMPLETE:
                        translation = AR_TO_EN_COMPLETE[msgid_text]
                        lines[i + 1] = f'msgstr "{translation}"\n'
                        translated_count += 1
                        print(f"  ✅ {msgid_text} → {translation}")
        
        i += 1
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\n📊 Translated {translated_count} strings")
    return translated_count


def main():
    """Main function"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    en_po = os.path.join(base_dir, 'locale', 'en', 'LC_MESSAGES', 'django.po')
    
    print("="*60)
    print("🌍 Complete Arabic to English Translation")
    print("="*60)
    
    if os.path.exists(en_po):
        count = translate_po_file(en_po)
        print("\n" + "="*60)
        print(f"✅ Translation Complete! ({count} strings)")
        print("="*60)
        print("\n🔄 Next step: Run 'python manage.py compilemessages'")
    else:
        print(f"❌ File not found: {en_po}")


if __name__ == '__main__':
    main()

