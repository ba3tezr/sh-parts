#!/usr/bin/env python3
import re
import os

# قائمة الملفات التي تحتوي على نماذج
modal_files = [
    'templates/pages/sales.html',
    'templates/pages/inventory_count.html',
    'templates/pages/customers_enhanced.html',
    'templates/pages/category_management.html',
    'templates/pages/warehouse_management.html',
    'templates/pages/barcode_system.html',
    'templates/pages/location_transfer.html',
]

print("=" * 70)
print("🔍 فحص النماذج (Modals) في المشروع")
print("=" * 70)
print()

for file_path in modal_files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن عناوين النماذج غير المترجمة
    # نبحث عن modal-title بدون data-translate أو {% trans %}
    patterns = [
        (r'<h5 class="modal-title">[^<]*[ا-ي][^<]*</h5>', 'عنوان نموذج غير مترجم'),
        (r'<button[^>]*class="btn[^"]*"[^>]*>[^<]*[ا-ي][^<]*</button>', 'زر غير مترجم'),
        (r'<label[^>]*>[^<]*[ا-ي][^<]*</label>', 'label غير مترجم'),
    ]
    
    issues = []
    for pattern, desc in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            # تجاهل إذا كان يحتوي على data-translate أو {% trans %}
            if 'data-translate' not in match and '{% trans %}' not in match and '{% trans "' not in match:
                issues.append((desc, match[:80]))
    
    if issues:
        print(f"📄 {file_path}")
        print(f"   وجد {len(issues)} مشكلة:")
        for desc, match in issues[:5]:  # أول 5 فقط
            print(f"   ⚠️ {desc}: {match}...")
        print()

print("=" * 70)
print("✅ انتهى الفحص")
print("=" * 70)
