#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove ALL fuzzy flags from .po files
Fuzzy translations are IGNORED by Django!
"""

import re

def remove_fuzzy_flags(po_file_path):
    """
    Remove all #, fuzzy flags from .po file
    """
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    removed_count = 0
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a fuzzy flag
        if line.strip().startswith('#, fuzzy'):
            # Skip this line (remove it)
            removed_count += 1
            
            # Also skip the #| msgid line if it exists (old reference)
            if i + 1 < len(lines) and lines[i + 1].strip().startswith('#|'):
                i += 1  # Skip the reference line too
            
            i += 1
            continue
        
        # Check for old reference lines #| msgid "..."
        if line.strip().startswith('#|'):
            # Skip old reference lines
            i += 1
            continue
        
        # Keep this line
        new_lines.append(line)
        i += 1
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return removed_count


def main():
    print("=" * 80)
    print("🔧 Removing ALL Fuzzy Flags from .po files")
    print("=" * 80)
    print()
    print("⚠️  Fuzzy translations are IGNORED by Django!")
    print("⚠️  This is why your translations don't appear!")
    print()
    
    # Remove from English file
    print("📝 Processing: locale/en/LC_MESSAGES/django.po")
    en_removed = remove_fuzzy_flags('locale/en/LC_MESSAGES/django.po')
    print(f"  ✅ Removed {en_removed} fuzzy flags")
    print()
    
    # Remove from Arabic file
    print("📝 Processing: locale/ar/LC_MESSAGES/django.po")
    ar_removed = remove_fuzzy_flags('locale/ar/LC_MESSAGES/django.po')
    print(f"  ✅ Removed {ar_removed} fuzzy flags")
    print()
    
    print("=" * 80)
    print(f"✅ Total: {ar_removed + en_removed} fuzzy flags removed")
    print("=" * 80)
    print()
    print("🔄 CRITICAL Next steps:")
    print("  1. python manage.py compilemessages")
    print("  2. Restart Django server (MUST!)")
    print("  3. Clear browser cache (Ctrl+Shift+R)")
    print("  4. Test translations!")
    print()


if __name__ == '__main__':
    main()
