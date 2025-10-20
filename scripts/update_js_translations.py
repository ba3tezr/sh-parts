#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to update JavaScript translations in templates
Replaces hardcoded Arabic strings with t() function calls
"""

import re
import os
import glob

# Translation mapping for common JavaScript strings
JS_TRANSLATIONS = {
    # Alerts and confirmations
    'فشل الوصول إلى الكاميرا': 'camera_access_failed',
    'الرجاء اختيار قطعة واحدة على الأقل': 'select_at_least_one_item',
    'الرجاء مسح باركود أولاً': 'scan_barcode_first',
    'ميزة التعديل السريع قيد التطوير': 'quick_edit_in_development',
    'ميزة البيع السريع قيد التطوير': 'quick_sale_in_development',
    'تم إضافة الفئة بنجاح': 'category_added_successfully',
    'فشل إضافة الفئة': 'failed_to_add_category',
    'حدث خطأ أثناء إضافة الفئة': 'error_adding_category',
    'تم تحديث الفئة بنجاح': 'category_updated_successfully',
    'فشل تحديث الفئة': 'failed_to_update_category',
    'حدث خطأ أثناء تحديث الفئة': 'error_updating_category',
    'تم حذف الفئة بنجاح': 'category_deleted_successfully',
    'فشل حذف الفئة': 'failed_to_delete_category',
    'حدث خطأ أثناء حذف الفئة': 'error_deleting_category',
    
    # Common messages
    'جاري التحميل...': 'loading',
    'تم الحفظ بنجاح': 'saved_successfully',
    'حدث خطأ': 'error_occurred',
    'هل أنت متأكد؟': 'are_you_sure',
    'تم الحذف بنجاح': 'deleted_successfully',
    'فشل الحذف': 'failed_to_delete',
    'تم التحديث بنجاح': 'updated_successfully',
    'فشل التحديث': 'failed_to_update',
    'تم الإضافة بنجاح': 'added_successfully',
    'فشل الإضافة': 'failed_to_add',
    'لا توجد بيانات': 'no_data',
    'الرجاء الانتظار': 'please_wait',
    'تم النسخ': 'copied',
    'فشل النسخ': 'copy_failed',
}


def update_js_in_template(file_path):
    """
    Update JavaScript translations in a template file
    """
    print(f"\n📝 Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    updated_count = 0
    
    # Find all alert() calls with Arabic text
    alert_pattern = r"alert\(['\"]([^'\"]+)['\"]\)"
    
    def replace_alert(match):
        nonlocal updated_count
        text = match.group(1)
        
        # Skip if already using trans tag
        if '{% trans' in text or 't(' in text:
            return match.group(0)
        
        # Check if we have a translation key for this text
        if text in JS_TRANSLATIONS:
            key = JS_TRANSLATIONS[text]
            updated_count += 1
            print(f"  ✅ alert('{text}') → alert(t('{key}'))")
            return f"alert(t('{key}'))"
        
        return match.group(0)
    
    content = re.sub(alert_pattern, replace_alert, content)
    
    # Find all confirm() calls with Arabic text
    confirm_pattern = r"confirm\(['\"]([^'\"]+)['\"]\)"
    
    def replace_confirm(match):
        nonlocal updated_count
        text = match.group(1)
        
        # Skip if already using trans tag
        if '{% trans' in text or 't(' in text:
            return match.group(0)
        
        # Check if we have a translation key for this text
        if text in JS_TRANSLATIONS:
            key = JS_TRANSLATIONS[text]
            updated_count += 1
            print(f"  ✅ confirm('{text}') → confirm(t('{key}'))")
            return f"confirm(t('{key}'))"
        
        return match.group(0)
    
    content = re.sub(confirm_pattern, replace_confirm, content)
    
    # Write back if changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  📊 Updated {updated_count} translations")
        return updated_count
    else:
        print(f"  ℹ️  No changes needed")
        return 0


def update_json_translations():
    """
    Add new translation keys to ar.json and en.json
    """
    import json
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Arabic translations
    ar_json_path = os.path.join(base_dir, 'static', 'js', 'translations', 'ar.json')
    with open(ar_json_path, 'r', encoding='utf-8') as f:
        ar_data = json.load(f)
    
    # Add new keys
    new_ar_keys = {
        'camera_access_failed': 'فشل الوصول إلى الكاميرا',
        'select_at_least_one_item': 'الرجاء اختيار قطعة واحدة على الأقل',
        'scan_barcode_first': 'الرجاء مسح باركود أولاً',
        'quick_edit_in_development': 'ميزة التعديل السريع قيد التطوير',
        'quick_sale_in_development': 'ميزة البيع السريع قيد التطوير',
        'category_added_successfully': 'تم إضافة الفئة بنجاح',
        'failed_to_add_category': 'فشل إضافة الفئة',
        'error_adding_category': 'حدث خطأ أثناء إضافة الفئة',
        'category_updated_successfully': 'تم تحديث الفئة بنجاح',
        'failed_to_update_category': 'فشل تحديث الفئة',
        'error_updating_category': 'حدث خطأ أثناء تحديث الفئة',
        'category_deleted_successfully': 'تم حذف الفئة بنجاح',
        'failed_to_delete_category': 'فشل حذف الفئة',
        'error_deleting_category': 'حدث خطأ أثناء حذف الفئة',
    }
    
    ar_data.update(new_ar_keys)
    
    with open(ar_json_path, 'w', encoding='utf-8') as f:
        json.dump(ar_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Updated {ar_json_path} with {len(new_ar_keys)} new keys")
    
    # English translations
    en_json_path = os.path.join(base_dir, 'static', 'js', 'translations', 'en.json')
    with open(en_json_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    new_en_keys = {
        'camera_access_failed': 'Failed to access camera',
        'select_at_least_one_item': 'Please select at least one item',
        'scan_barcode_first': 'Please scan barcode first',
        'quick_edit_in_development': 'Quick edit feature is under development',
        'quick_sale_in_development': 'Quick sale feature is under development',
        'category_added_successfully': 'Category added successfully',
        'failed_to_add_category': 'Failed to add category',
        'error_adding_category': 'Error adding category',
        'category_updated_successfully': 'Category updated successfully',
        'failed_to_update_category': 'Failed to update category',
        'error_updating_category': 'Error updating category',
        'category_deleted_successfully': 'Category deleted successfully',
        'failed_to_delete_category': 'Failed to delete category',
        'error_deleting_category': 'Error deleting category',
    }
    
    en_data.update(new_en_keys)
    
    with open(en_json_path, 'w', encoding='utf-8') as f:
        json.dump(en_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Updated {en_json_path} with {len(new_en_keys)} new keys")


def main():
    """Main function"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.join(base_dir, 'templates', 'pages')
    
    print("="*60)
    print("🔄 Updating JavaScript Translations in Templates")
    print("="*60)
    
    # Find all HTML files
    html_files = glob.glob(os.path.join(templates_dir, '*.html'))
    
    total_updated = 0
    for html_file in html_files:
        count = update_js_in_template(html_file)
        total_updated += count
    
    print("\n" + "="*60)
    print(f"✅ Updated {total_updated} JavaScript translations in {len(html_files)} files")
    print("="*60)
    
    # Update JSON translation files
    print("\n" + "="*60)
    print("📝 Updating JSON Translation Files")
    print("="*60)
    update_json_translations()
    
    print("\n" + "="*60)
    print("✅ All Done!")
    print("="*60)


if __name__ == '__main__':
    main()

