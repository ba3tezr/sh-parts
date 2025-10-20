#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to test translation completeness
"""

import os
import sys
import json
import re

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_po_files():
    """Test .po files"""
    print("\n" + "="*60)
    print("📝 Testing .po Files")
    print("="*60)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Test Arabic .po
    ar_po = os.path.join(base_dir, 'locale', 'ar', 'LC_MESSAGES', 'django.po')
    if os.path.exists(ar_po):
        with open(ar_po, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count msgid and msgstr
        msgid_count = len(re.findall(r'^msgid "', content, re.MULTILINE))
        empty_msgstr = len(re.findall(r'^msgstr ""$', content, re.MULTILINE))
        
        print(f"\n🇸🇦 Arabic (.po):")
        print(f"  - Total msgid: {msgid_count}")
        print(f"  - Empty msgstr: {empty_msgstr}")
        print(f"  - Translated: {msgid_count - empty_msgstr}")
        print(f"  - Progress: {((msgid_count - empty_msgstr) / msgid_count * 100):.1f}%")
    
    # Test English .po
    en_po = os.path.join(base_dir, 'locale', 'en', 'LC_MESSAGES', 'django.po')
    if os.path.exists(en_po):
        with open(en_po, 'r', encoding='utf-8') as f:
            content = f.read()
        
        msgid_count = len(re.findall(r'^msgid "', content, re.MULTILINE))
        empty_msgstr = len(re.findall(r'^msgstr ""$', content, re.MULTILINE))
        
        print(f"\n🇬🇧 English (.po):")
        print(f"  - Total msgid: {msgid_count}")
        print(f"  - Empty msgstr: {empty_msgstr}")
        print(f"  - Translated: {msgid_count - empty_msgstr}")
        print(f"  - Progress: {((msgid_count - empty_msgstr) / msgid_count * 100):.1f}%")
    
    # Check .mo files exist
    ar_mo = os.path.join(base_dir, 'locale', 'ar', 'LC_MESSAGES', 'django.mo')
    en_mo = os.path.join(base_dir, 'locale', 'en', 'LC_MESSAGES', 'django.mo')
    
    print(f"\n📦 Compiled Files:")
    print(f"  - Arabic .mo: {'✅ Exists' if os.path.exists(ar_mo) else '❌ Missing'}")
    print(f"  - English .mo: {'✅ Exists' if os.path.exists(en_mo) else '❌ Missing'}")


def test_json_files():
    """Test JSON translation files"""
    print("\n" + "="*60)
    print("📝 Testing JSON Translation Files")
    print("="*60)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Test ar.json
    ar_json = os.path.join(base_dir, 'static', 'js', 'translations', 'ar.json')
    if os.path.exists(ar_json):
        with open(ar_json, 'r', encoding='utf-8') as f:
            ar_data = json.load(f)
        
        print(f"\n🇸🇦 Arabic (ar.json):")
        print(f"  - Total keys: {len(ar_data)}")
        print(f"  - Sample keys: {list(ar_data.keys())[:5]}")
    
    # Test en.json
    en_json = os.path.join(base_dir, 'static', 'js', 'translations', 'en.json')
    if os.path.exists(en_json):
        with open(en_json, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
        
        print(f"\n🇬🇧 English (en.json):")
        print(f"  - Total keys: {len(en_data)}")
        print(f"  - Sample keys: {list(en_data.keys())[:5]}")
    
    # Check if keys match
    if os.path.exists(ar_json) and os.path.exists(en_json):
        ar_keys = set(ar_data.keys())
        en_keys = set(en_data.keys())
        
        missing_in_en = ar_keys - en_keys
        missing_in_ar = en_keys - ar_keys
        
        print(f"\n🔍 Key Comparison:")
        print(f"  - Keys in both: {len(ar_keys & en_keys)}")
        print(f"  - Missing in English: {len(missing_in_en)}")
        print(f"  - Missing in Arabic: {len(missing_in_ar)}")
        
        if missing_in_en:
            print(f"  - Missing in EN: {list(missing_in_en)[:5]}")
        if missing_in_ar:
            print(f"  - Missing in AR: {list(missing_in_ar)[:5]}")


def test_templates():
    """Test templates for {% trans %} usage"""
    print("\n" + "="*60)
    print("📝 Testing Templates")
    print("="*60)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.join(base_dir, 'templates', 'pages')
    
    if not os.path.exists(templates_dir):
        print("❌ Templates directory not found")
        return
    
    total_files = 0
    files_with_trans = 0
    files_with_i18n = 0
    
    for filename in os.listdir(templates_dir):
        if filename.endswith('.html'):
            total_files += 1
            filepath = os.path.join(templates_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            has_i18n = '{% load i18n %}' in content or '{% load static i18n %}' in content
            has_trans = '{% trans' in content
            
            if has_i18n:
                files_with_i18n += 1
            if has_trans:
                files_with_trans += 1
    
    print(f"\n📊 Template Statistics:")
    print(f"  - Total HTML files: {total_files}")
    print(f"  - Files with {{% load i18n %}}: {files_with_i18n}")
    print(f"  - Files with {{% trans %}}: {files_with_trans}")
    print(f"  - Coverage: {(files_with_trans / total_files * 100):.1f}%")


def test_login_page():
    """Test login page specifically"""
    print("\n" + "="*60)
    print("📝 Testing Login Page")
    print("="*60)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    login_file = os.path.join(base_dir, 'templates', 'pages', 'login.html')
    
    if not os.path.exists(login_file):
        print("❌ Login page not found")
        return
    
    with open(login_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        'load i18n tag': ('{% load i18n %}' in content or '{% load static i18n %}' in content),
        'Language switcher': 'lang-switcher' in content,
        'trans tag': '{% trans' in content,
        'RTL/LTR support': 'dir=' in content,
        'Language buttons': 'data-lang=' in content,
    }
    
    print(f"\n✅ Login Page Checks:")
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check}")


def main():
    """Main function"""
    print("\n" + "="*60)
    print("🧪 SH Parts Translation Test Suite")
    print("="*60)
    
    test_po_files()
    test_json_files()
    test_templates()
    test_login_page()
    
    print("\n" + "="*60)
    print("✅ Test Complete!")
    print("="*60)
    print("\n💡 Next Steps:")
    print("  1. Start the development server: python manage.py runserver")
    print("  2. Open http://localhost:8000/login/")
    print("  3. Test language switching")
    print("  4. Navigate through all pages in both languages")
    print("\n")


if __name__ == '__main__':
    main()

