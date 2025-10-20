#!/usr/bin/env python3
"""
Complete remaining translations with comprehensive dictionary
"""

import re

# Comprehensive translation dictionaries
AR_TO_EN = {
    # Technical/Model fields
    "last login": "آخر تسجيل دخول",
    "2FA enabled": "المصادقة الثنائية مفعلة",
    "2FA secret": "رمز المصادقة الثنائية",
    "car make": "ماركة السيارة",
    "car makes": "ماركات السيارات",
    "production start year": "سنة بداية الإنتاج",
    "production end year": "سنة نهاية الإنتاج",
    "body type": "نوع الهيكل",
    "car model": "موديل السيارة",
    "car models": "موديلات السيارات",
    "category name": "اسم الفئة",
    "category name (Arabic)": "اسم الفئة (بالعربية)",
    "parent category": "الفئة الأم",
    "icon class": "رمز الأيقونة",
    "sort order": "ترتيب العرض",
    "part category": "فئة القطعة",
    "part categories": "فئات القطع",
    "part number": "رقم القطعة",
    "description (Arabic)": "الوصف (بالعربية)",
    "compatible models": "الموديلات المتوافقة",
    "default image": "الصورة الافتراضية",
    "universal part": "قطعة عامة",
    "parts": "القطع",
    "Excellent": "ممتاز",
    "Good": "جيد",
    "Fair": "مقبول",
    "Poor": "سيئ",
    "Salvage": "للإنقاذ",
    "intake notes": "ملاحظات الاستلام",
    "received by": "مستلم بواسطة",
    "dismantled": "مفكك",
    "dismantled date": "تاريخ التفكيك",
    "vehicles": "السيارات",
    "image": "الصورة",
    "caption": "التعليق",
    "primary photo": "الصورة الأساسية",
    "uploaded at": "رفع في",
    "vehicle photo": "صورة السيارة",
    "vehicle photos": "صور السيارة",
    "Address": "العنوان",
    "Financial": "المالية",
    "Additional": "إضافي",
    "Note": "ملاحظة",
    "Business": "تجاري",
    "business name": "اسم النشاط التجاري",
    "secondary phone": "هاتف ثانوي",
    "address line 1": "سطر العنوان 1",
    "address line 2": "سطر العنوان 2",
    "state/province": "المحافظة/الولاية",
    "Superuser must have is_staff=True.": "المستخدم الرئيسي يجب أن يكون is_staff=True.",
    "Superuser must have is_superuser=True.": "المستخدم الرئيسي يجب أن يكون is_superuser=True.",
    "make name (Arabic)": "اسم الماركة (بالعربية)",
    "model name (Arabic)": "اسم الموديل (بالعربية)",
    "part name (Arabic)": "اسم القطعة (بالعربية)",
    "Location & Tracking": "الموقع والتتبع",
    "Used - Excellent": "مستعمل - ممتاز",
    "Used - Good": "مستعمل - جيد",
    "Used - Fair": "مستعمل - مقبول",
    "discount %": "نسبة الخصم %",
    "Credit/Debit Card": "بطاقة ائتمان/خصم",
    
    # Theme names - bilingual, keep as is
    "الثيم الأزرق النهاري / Day Blue Theme": "Day Blue Theme / الثيم الأزرق النهاري",
    "الثيم الأزرق الداكن / Dark Blue Theme": "Dark Blue Theme / الثيم الأزرق الداكن",
    "الثيم الفاتح / Light Theme": "Light Theme / الثيم الفاتح",
    "ثيم الرمال الذهبية / Camel Dune Theme": "Camel Dune Theme / ثيم الرمال الذهبية",
    "الثيم الزيتي / Olive Sage Theme": "Olive Sage Theme / الثيم الزيتي",
    
    # Messages
    "تحديث جديد متاح! هل تريد تحديث التطبيق؟": "New update available! Do you want to update the app?",
}

EN_TO_AR = {
    "Superuser must have is_staff=True.": "المستخدم الرئيسي يجب أن يكون is_staff=True.",
    "Superuser must have is_superuser=True.": "المستخدم الرئيسي يجب أن يكون is_superuser=True.",
    "2FA enabled": "المصادقة الثنائية مفعلة",
    "2FA secret": "رمز المصادقة الثنائية",
    "make name (Arabic)": "اسم الماركة (بالعربية)",
    "model name (Arabic)": "اسم الموديل (بالعربية)",
    "category name (Arabic)": "اسم الفئة (بالعربية)",
    "part name (Arabic)": "اسم القطعة (بالعربية)",
    "description (Arabic)": "الوصف (بالعربية)",
    "address line 1": "سطر العنوان 1",
    "address line 2": "سطر العنوان 2",
    "state/province": "المحافظة/الولاية",
    "Location & Tracking": "الموقع والتتبع",
    "Used - Excellent": "مستعمل - ممتاز",
    "Used - Good": "مستعمل - جيد",
    "Used - Fair": "مستعمل - مقبول",
    "discount %": "نسبة الخصم %",
    "Credit/Debit Card": "بطاقة ائتمان/خصم",
    
    # Theme names
    "الثيم الأزرق النهاري / Day Blue Theme": "الثيم الأزرق النهاري / Day Blue Theme",
    "الثيم الأزرق الداكن / Dark Blue Theme": "الثيم الأزرق الداكن / Dark Blue Theme",
    "الثيم الفاتح / Light Theme": "الثيم الفاتح / Light Theme",
    "ثيم الرمال الذهبية / Camel Dune Theme": "ثيم الرمال الذهبية / Camel Dune Theme",
    "الثيم الزيتي / Olive Sage Theme": "الثيم الزيتي / Olive Sage Theme",
    
    "تحديث جديد متاح! هل تريد تحديث التطبيق؟": "تحديث جديد متاح! هل تريد تحديث التطبيق؟",
}


def translate_po_file(po_file_path, dictionary, language_name):
    """
    Translate empty msgstr using dictionary
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
                        print(f"  ✅ {msgid_text[:50]}... → {translation[:50]}...")
        
        i += 1
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return changes


def main():
    print("=" * 70)
    print("🌍 Completing Remaining Translations")
    print("=" * 70)
    print()
    
    # Translate English file (AR to EN)
    print("📝 Processing: locale/en/LC_MESSAGES/django.po (Arabic → English)")
    en_changes = translate_po_file('locale/en/LC_MESSAGES/django.po', AR_TO_EN, 'English')
    print(f"  ✅ Translated {en_changes} strings")
    print()
    
    # Translate Arabic file (EN to AR)
    print("📝 Processing: locale/ar/LC_MESSAGES/django.po (English → Arabic)")
    ar_changes = translate_po_file('locale/ar/LC_MESSAGES/django.po', EN_TO_AR, 'Arabic')
    print(f"  ✅ Translated {ar_changes} strings")
    print()
    
    print("=" * 70)
    print(f"✅ Total: {ar_changes + en_changes} translations completed")
    print("=" * 70)
    print()
    print("🔄 Next step: Run 'python manage.py compilemessages'")


if __name__ == '__main__':
    main()
