#!/usr/bin/env python3
"""
Translate English strings to Arabic in locale/ar/LC_MESSAGES/django.po
"""

import re
import sys

# English to Arabic translation dictionary
EN_TO_AR = {
    # Language names
    "English": "الإنجليزية",
    "Arabic": "العربية",
    
    # Names (keep as is or translate)
    "Zakee Tahawi": "زكي طحاوي",
    
    # Common UI
    "Remember me": "تذكرني",
    "Default credentials": "البيانات الافتراضية",
    "Developed by": "تطوير",
    "All Rights Reserved": "جميع الحقوق محفوظة",
}


def translate_po_file(po_file_path):
    """Translate English msgid to Arabic msgstr in .po file"""
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    translated_count = 0
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Find msgid with English text
        if line.startswith('msgid "') and not line.startswith('msgid ""'):
            msgid_match = re.match(r'msgid "(.*)"', line)
            if msgid_match:
                msgid_text = msgid_match.group(1)
                
                # Check if next line is empty msgstr
                if i + 1 < len(lines) and lines[i + 1].strip() == 'msgstr ""':
                    # Try to find translation
                    if msgid_text in EN_TO_AR:
                        translation = EN_TO_AR[msgid_text]
                        lines[i + 1] = f'msgstr "{translation}"\n'
                        print(f"  ✅ {msgid_text} → {translation}")
                        translated_count += 1
        
        i += 1
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return translated_count


def main():
    """Main function"""
    
    po_file = 'locale/ar/LC_MESSAGES/django.po'
    
    print("=" * 60)
    print("🌍 English to Arabic Translation")
    print("=" * 60)
    print()
    print(f"📝 Processing: {po_file}")
    
    count = translate_po_file(po_file)
    
    print()
    print(f"📊 Translated {count} strings")
    print()
    print("=" * 60)
    print(f"✅ Translation Complete! ({count} strings)")
    print("=" * 60)
    print()
    print("🔄 Next step: Run 'python manage.py compilemessages'")


if __name__ == '__main__':
    main()

