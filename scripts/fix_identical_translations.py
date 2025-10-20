#!/usr/bin/env python3
"""
Fix identical translations where msgid should equal msgstr
"""

import re

def fix_identical_translations(po_file_path, language):
    """
    Fix translations where msgid and msgstr should be identical
    """
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all msgid followed by empty msgstr
    pattern = r'msgid "([^"]+)"\nmsgstr ""'
    
    # Special cases that should remain identical
    identical_cases = []
    
    if language == 'ar':
        # Arabic file: Arabic words should stay Arabic
        identical_cases = [
            # Arabic language names and proper nouns that should stay in Arabic
            r'[\u0600-\u06FF\s]+',  # Any Arabic text
        ]
    elif language == 'en':
        # English file: English words should stay English
        identical_cases = [
            # English words that should stay English
            r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$',  # Capitalized words (proper nouns)
            r'^[A-Z]+$',  # All caps abbreviations
        ]
    
    changes = 0
    
    # Find all empty msgstr entries
    matches = list(re.finditer(pattern, content))
    
    for match in reversed(matches):  # Reverse to maintain positions
        msgid_text = match.group(1)
        
        # Check if this msgid should have identical msgstr
        should_be_identical = False
        
        if language == 'ar':
            # In Arabic file, if msgid is Arabic, msgstr should also be Arabic
            if re.search(r'[\u0600-\u06FF]', msgid_text):
                # Check if it's a pure Arabic phrase (no English mixed)
                if not re.search(r'[A-Za-z]{3,}', msgid_text):
                    should_be_identical = True
        
        elif language == 'en':
            # In English file, if msgid is English, msgstr should also be English
            if re.search(r'^[A-Za-z\s]+$', msgid_text):
                # Check if it's a pure English phrase (no Arabic mixed)
                if not re.search(r'[\u0600-\u06FF]', msgid_text):
                    should_be_identical = True
        
        if should_be_identical:
            # Replace empty msgstr with identical msgid
            old_text = match.group(0)
            new_text = f'msgid "{msgid_text}"\nmsgstr "{msgid_text}"'
            content = content[:match.start()] + new_text + content[match.end():]
            changes += 1
            print(f"  ✅ Fixed: {msgid_text}")
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return changes


def main():
    print("=" * 60)
    print("🔧 Fixing Identical Translations")
    print("=" * 60)
    print()
    
    # Fix Arabic file
    print("📝 Processing: locale/ar/LC_MESSAGES/django.po")
    ar_changes = fix_identical_translations('locale/ar/LC_MESSAGES/django.po', 'ar')
    print(f"  ✅ Fixed {ar_changes} identical translations")
    print()
    
    # Fix English file
    print("📝 Processing: locale/en/LC_MESSAGES/django.po")
    en_changes = fix_identical_translations('locale/en/LC_MESSAGES/django.po', 'en')
    print(f"  ✅ Fixed {en_changes} identical translations")
    print()
    
    print("=" * 60)
    print(f"✅ Total: {ar_changes + en_changes} translations fixed")
    print("=" * 60)
    print()
    print("🔄 Next step: Run 'python manage.py compilemessages'")


if __name__ == '__main__':
    main()
