#!/usr/bin/env python3
"""
Add {% load i18n %} to all HTML templates that don't have it
"""

import os
import re
from pathlib import Path

def add_i18n_to_template(file_path):
    """Add {% load i18n %} to a template file if it doesn't have it"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has i18n in any load tag
    if re.search(r'{%\s*load\s+[^%]*i18n', content):
        return False, "Already has i18n"

    # Check if it's a Django template (has {% or {{)
    if not ('{%' in content or '{{' in content):
        return False, "Not a Django template"
    
    # Find the first {% load ... %} tag
    load_match = re.search(r'{%\s*load\s+[^%]+%}', content)
    
    if load_match:
        # Add i18n to existing load tag
        existing_load = load_match.group(0)
        # Extract what's being loaded
        load_content = re.search(r'{%\s*load\s+([^%]+)%}', existing_load).group(1).strip()
        # Add i18n if not already there
        if 'i18n' not in load_content:
            new_load = f"{{% load {load_content} i18n %}}"
            content = content.replace(existing_load, new_load, 1)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, f"Added i18n to existing load: {existing_load}"
    else:
        # No load tag found, add one at the beginning
        # Find first line after <!DOCTYPE or <html or {%
        lines = content.split('\n')
        insert_line = 0
        
        for i, line in enumerate(lines):
            if line.strip().startswith('<!DOCTYPE') or line.strip().startswith('<html'):
                insert_line = i + 1
                break
            elif line.strip().startswith('{%') and 'extends' in line:
                insert_line = i + 1
                break
        
        # Insert {% load i18n %} at the appropriate line
        lines.insert(insert_line, '{% load i18n %}')
        content = '\n'.join(lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, f"Added new load tag at line {insert_line}"
    
    return False, "No changes needed"


def main():
    """Process all HTML templates"""
    
    print("=" * 60)
    print("🌍 Adding {% load i18n %} to all templates")
    print("=" * 60)
    print()
    
    templates_dir = Path('templates')
    html_files = list(templates_dir.rglob('*.html'))
    
    print(f"📁 Found {len(html_files)} HTML files")
    print()
    
    modified_count = 0
    skipped_count = 0
    
    for html_file in sorted(html_files):
        modified, reason = add_i18n_to_template(html_file)
        
        if modified:
            print(f"  ✅ {html_file}: {reason}")
            modified_count += 1
        else:
            print(f"  ⏭️  {html_file}: {reason}")
            skipped_count += 1
    
    print()
    print("=" * 60)
    print(f"✅ Modified: {modified_count} files")
    print(f"⏭️  Skipped: {skipped_count} files")
    print("=" * 60)
    print()
    print("🔄 Next steps:")
    print("  1. Run: python manage.py makemessages -l ar -l en --ignore=venv --ignore=staticfiles")
    print("  2. Translate the new strings in locale/*/LC_MESSAGES/django.po")
    print("  3. Run: python manage.py compilemessages")


if __name__ == '__main__':
    main()

