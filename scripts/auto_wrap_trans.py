#!/usr/bin/env python3
"""
Automatically wrap translatable strings with {% trans %} in templates
"""

import re
import sys
from pathlib import Path

def has_arabic(text):
    """Check if text contains Arabic characters"""
    return bool(re.search(r'[\u0600-\u06FF]', text))

def has_english(text):
    """Check if text contains English letters (2+ consecutive)"""
    return bool(re.search(r'[A-Za-z]{2,}', text))

def should_translate(text):
    """Determine if text should be translated"""
    text = text.strip()
    
    # Skip empty or too short
    if len(text) < 2:
        return False
    
    # Skip if only numbers/symbols
    if text.isdigit() or not (has_arabic(text) or has_english(text)):
        return False
    
    # Skip usernames, emails, URLs
    if '@' in text or 'http' in text.lower() or text in ['admin', 'user', 'test']:
        return False
    
    # Skip placeholders with only variables
    if text.startswith('{{') and text.endswith('}}'):
        return False
    
    # Skip CSS/JS code
    if any(x in text for x in ['px', 'rem', 'function', 'var ', 'const ', '()', '=>']):
        return False
    
    return True

def wrap_text_nodes(content, file_path):
    """Wrap text nodes with {% trans %}"""
    
    changes = 0
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        original_line = line
        
        # Skip lines that already have {% trans %} or {% blocktrans %}
        if '{% trans' in line or '{% blocktrans' in line or '{%trans' in line:
            new_lines.append(line)
            continue
        
        # Skip HTML comments
        if '<!--' in line:
            new_lines.append(line)
            continue
        
        # Pattern: >Text< (text between tags)
        # Match text between > and < that's not a tag itself
        def replace_text_content(match):
            nonlocal changes
            before = match.group(1)  # The '>'
            text = match.group(2)
            after = match.group(3)   # The '<'
            
            text_stripped = text.strip()
            
            # Skip if empty or already translated
            if not text_stripped or '{{' in text or '{%' in text:
                return match.group(0)
            
            # Skip if shouldn't translate
            if not should_translate(text_stripped):
                return match.group(0)
            
            # Wrap with {% trans %}
            changes += 1
            # Preserve leading/trailing whitespace
            leading = text[:len(text) - len(text.lstrip())]
            trailing = text[len(text.rstrip()):]
            return f'{before}{leading}{{% trans "{text_stripped}" %}}{trailing}{after}'
        
        # Apply pattern
        line = re.sub(
            r'(>)([^<{]+)(<)',
            replace_text_content,
            line
        )
        
        new_lines.append(line)
    
    return '\n'.join(new_lines), changes

def wrap_attributes(content, file_path):
    """Wrap placeholder, title, and value attributes"""
    
    changes = 0
    
    # Pattern for placeholder="text"
    def replace_placeholder(match):
        nonlocal changes
        attr_name = match.group(1)
        text = match.group(2)
        
        if not should_translate(text):
            return match.group(0)
        
        # Check if already using {% trans %}
        if '{% trans' in match.group(0):
            return match.group(0)
        
        changes += 1
        return f'{attr_name}="{{% trans \'{text}\' %}}"'
    
    # Replace placeholder
    content = re.sub(
        r'(placeholder)="([^"]+)"',
        replace_placeholder,
        content
    )
    
    # Replace title (but not in <title> tag)
    content = re.sub(
        r'(?<!<)(title)="([^"]+)"',
        replace_placeholder,
        content
    )
    
    return content, changes

def process_template(file_path):
    """Process a single template file"""
    
    print(f"\n📄 Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        total_changes = 0
        
        # Wrap text nodes
        content, changes1 = wrap_text_nodes(content, file_path)
        total_changes += changes1
        
        # Wrap attributes
        content, changes2 = wrap_attributes(content, file_path)
        total_changes += changes2
        
        if total_changes > 0:
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Wrapped {total_changes} strings")
            return total_changes
        else:
            print(f"  ⏭️  No changes needed")
            return 0
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return 0

def main():
    if len(sys.argv) > 1:
        # Process specific file
        file_path = Path(sys.argv[1])
        if file_path.exists():
            changes = process_template(file_path)
            print(f"\n✅ Total: {changes} changes")
        else:
            print(f"❌ File not found: {file_path}")
    else:
        # Process all templates
        print("=" * 70)
        print("🌍 Auto-wrapping translatable strings with {% trans %}")
        print("=" * 70)
        
        templates_dir = Path('templates/pages')
        html_files = list(templates_dir.glob('*.html'))
        
        print(f"\n📁 Found {len(html_files)} template files")
        
        total_changes = 0
        processed = 0
        
        for html_file in sorted(html_files):
            changes = process_template(html_file)
            if changes > 0:
                total_changes += changes
                processed += 1
        
        print("\n" + "=" * 70)
        print(f"✅ Processed {processed} files")
        print(f"✅ Total changes: {total_changes}")
        print("=" * 70)
        print("\n🔄 Next steps:")
        print("  1. Review the changes")
        print("  2. Run: python manage.py makemessages -l ar -l en")
        print("  3. Translate new strings in .po files")
        print("  4. Run: python manage.py compilemessages")

if __name__ == '__main__':
    main()
