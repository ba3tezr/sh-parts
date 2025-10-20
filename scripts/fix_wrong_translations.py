#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix WRONG translations in .po files - Complete correction
"""

import re

# Corrections for en/django.po (Arabic → English)
EN_CORRECTIONS = {
    # Login page - CRITICAL
    "اسم المستخدم": "Username",
    "كلمة المرور": "Password",
    "تذكرني": "Remember Me",
    "تسجيل الدخول": "Login",
    "البيانات الافتراضية: admin / admin123": "Default credentials: admin / admin123",
    "جميع الحقوق محفوظة": "All Rights Reserved",
    "تطوير": "Developed by",
    "Zakee Tahawi": "Zakee Tahawi",
    
    # System names
    "نظام قطع غيار السيارات": "Car Parts System",
    "نظام إدارة SH Parts": "SH Parts Management System",
    
    # Main menu
    "لوحة التحكم": "Dashboard",
    "لوحة الإدارة": "Admin Panel",
    "الملف الشخصي": "Profile",
    "الإعدادات": "Settings",
    "تسجيل الخروج": "Logout",
    
    # Common terms
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
    "التالي": "Next",
    "السابق": "Previous",
    
    # Categories
    "إدارة الفئات": "Category Management",
    "إدارة فئات القطع والسيارات": "Manage Parts and Vehicle Categories",
    "فئة جديدة": "New Category",
    "تصدير Excel": "Export Excel",
    "إجمالي الفئات": "Total Categories",
    "الفئات النشطة": "Active Categories",
    "إجمالي القطع": "Total Parts",
    "الحالة": "Status",
    "الكل": "All",
    "نشط": "Active",
    "غير نشط": "Inactive",
    "بحث...": "Search...",
    
    # Table headers
    "الاسم بالعربية": "Arabic Name",
    "الاسم بالإنجليزية": "English Name",
    "الوصف": "Description",
    "عدد القطع": "Parts Count",
    "الإجراءات": "Actions",
    
    # Forms
    "مثال: محرك": "Example: Engine",
    "Example: Engine": "Example: Engine",
    "وصف الفئة...": "Category description...",
    "تعديل الفئة": "Edit Category",
    "حفظ التغييرات": "Save Changes",
    
    # Loading/Messages
    "جاري التحميل...": "Loading...",
    "لا توجد بيانات": "No data available",
    "فشل تحميل البيانات": "Failed to load data",
    
    # Dates and time
    "اليوم": "Today",
    "أمس": "Yesterday",
    "هذا الأسبوع": "This Week",
    "هذا الشهر": "This Month",
    
    # Numbers
    "الأول": "First",
    "الثاني": "Second",
    "الثالث": "Third",
}

# Corrections for ar/django.po (English → Arabic) if any wrong
AR_CORRECTIONS = {
    "Username": "اسم المستخدم",
    "Password": "كلمة المرور",
    "Login": "تسجيل الدخول",
    "Remember Me": "تذكرني",
    "All Rights Reserved": "جميع الحقوق محفوظة",
    "Developed by": "تطوير",
    "Dashboard": "لوحة التحكم",
    "Profile": "الملف الشخصي",
    "Settings": "الإعدادات",
    "Logout": "تسجيل الخروج",
}


def fix_translations(po_file_path, corrections_dict, language_name):
    """
    Fix wrong translations in .po file
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
                
                # Check if this msgid needs correction
                if msgid_text in corrections_dict:
                    # Check next line (msgstr)
                    next_line = lines[i + 1]
                    if next_line.startswith('msgstr "'):
                        # Extract current msgstr
                        msgstr_match = re.match(r'msgstr "(.*)"', next_line)
                        if msgstr_match:
                            current_msgstr = msgstr_match.group(1)
                            correct_msgstr = corrections_dict[msgid_text]
                            
                            # Only update if different
                            if current_msgstr != correct_msgstr:
                                lines[i + 1] = f'msgstr "{correct_msgstr}"\n'
                                changes += 1
                                print(f"  ✅ {msgid_text[:35]:35} | {current_msgstr[:30]:30} → {correct_msgstr}")
        
        i += 1
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return changes


def main():
    print("=" * 90)
    print("🔧 Fixing WRONG Translations - Complete Correction")
    print("=" * 90)
    print()
    
    # Fix English file
    print("📝 Processing: locale/en/LC_MESSAGES/django.po (Arabic → English)")
    print("-" * 90)
    en_changes = fix_translations('locale/en/LC_MESSAGES/django.po', EN_CORRECTIONS, 'English')
    print(f"\n  ✅ Fixed {en_changes} wrong translations")
    print()
    
    # Fix Arabic file if needed
    print("📝 Processing: locale/ar/LC_MESSAGES/django.po (English → Arabic)")
    print("-" * 90)
    ar_changes = fix_translations('locale/ar/LC_MESSAGES/django.po', AR_CORRECTIONS, 'Arabic')
    print(f"\n  ✅ Fixed {ar_changes} wrong translations")
    print()
    
    print("=" * 90)
    print(f"✅ Total: {ar_changes + en_changes} translations corrected")
    print("=" * 90)
    print()
    print("🔄 Next step: Run 'python manage.py compilemessages'")


if __name__ == '__main__':
    main()
