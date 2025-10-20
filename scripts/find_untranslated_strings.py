#!/usr/bin/env python3
"""
Find all hardcoded strings in templates that should be translated
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def has_arabic(text):
    """Check if text contains Arabic characters"""
    return bool(re.search(r'[\u0600-\u06FF]', text))

def has_english_words(text):
    """Check if text contains English words (not just symbols)"""
    # Must have at least 2 consecutive English letters
    return bool(re.search(r'[A-Za-z]{2,}', text))

def extract_text_from_html(content):
    """Extract text content from HTML that might need translation"""
    
    untranslated = []
    
    # Pattern 1: Text between HTML tags (not in {% trans %})
    # Match: >Some Text<  but not >{% trans "..." %}<
    pattern1 = r'>([^<{]+)<'
    
    for match in re.finditer(pattern1, content):
        text = match.group(1).strip()
        
        # Skip if empty, only whitespace, or only numbers/symbols
        if not text or text.isspace() or text.isdigit():
            continue
        
        # Skip if it's a Django variable {{ ... }}
        if '{{' in text or '}}' in text:
            continue
        
        # Skip if it's already in {% trans %}
        start_pos = match.start()
        before = content[max(0, start_pos-50):start_pos]
        if '{% trans' in before or '{%trans' in before:
            continue
        
        # Check if it has Arabic or English
        if has_arabic(text) or has_english_words(text):
            untranslated.append({
                'text': text,
                'type': 'html_content',
                'context': content[max(0, start_pos-30):min(len(content), start_pos+50)]
            })
    
    # Pattern 2: Placeholder attributes
    pattern2 = r'placeholder=["\']([^"\']+)["\']'
    
    for match in re.finditer(pattern2, content):
        text = match.group(1).strip()
        
        if text and (has_arabic(text) or has_english_words(text)):
            # Check if it's already using {% trans %}
            if '{% trans' not in content[max(0, match.start()-20):match.end()+20]:
                untranslated.append({
                    'text': text,
                    'type': 'placeholder',
                    'context': match.group(0)
                })
    
    # Pattern 3: Title attributes
    pattern3 = r'title=["\']([^"\']+)["\']'
    
    for match in re.finditer(pattern3, content):
        text = match.group(1).strip()
        
        if text and (has_arabic(text) or has_english_words(text)):
            if '{% trans' not in content[max(0, match.start()-20):match.end()+20]:
                untranslated.append({
                    'text': text,
                    'type': 'title',
                    'context': match.group(0)
                })
    
    # Pattern 4: Value attributes in buttons/inputs
    pattern4 = r'value=["\']([^"\']+)["\']'
    
    for match in re.finditer(pattern4, content):
        text = match.group(1).strip()
        
        # Skip empty, numbers, or single characters
        if not text or text.isdigit() or len(text) < 2:
            continue
        
        if has_arabic(text) or has_english_words(text):
            if '{% trans' not in content[max(0, match.start()-20):match.end()+20]:
                untranslated.append({
                    'text': text,
                    'type': 'value',
                    'context': match.group(0)
                })
    
    return untranslated


def analyze_template(file_path):
    """Analyze a template file for untranslated strings"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return extract_text_from_html(content)


def main():
    """Process all HTML templates"""
    
    print("=" * 80)
    print("🔍 Finding Untranslated Strings in Templates")
    print("=" * 80)
    print()
    
    templates_dir = Path('templates')
    html_files = list(templates_dir.rglob('*.html'))
    
    print(f"📁 Analyzing {len(html_files)} HTML files...")
    print()
    
    all_findings = defaultdict(list)
    total_count = 0
    
    for html_file in sorted(html_files):
        untranslated = analyze_template(html_file)
        
        if untranslated:
            all_findings[str(html_file)] = untranslated
            total_count += len(untranslated)
    
    # Print results
    if not all_findings:
        print("✅ No untranslated strings found! All templates are properly internationalized.")
        return
    
    print(f"⚠️  Found {total_count} potentially untranslated strings in {len(all_findings)} files:")
    print()
    
    for file_path, findings in sorted(all_findings.items()):
        print(f"\n📄 {file_path} ({len(findings)} strings)")
        print("-" * 80)
        
        # Group by type
        by_type = defaultdict(list)
        for finding in findings:
            by_type[finding['type']].append(finding)
        
        for ftype, items in sorted(by_type.items()):
            print(f"\n  {ftype.upper()}:")
            for item in items[:10]:  # Limit to 10 per type
                text = item['text'][:60]
                if len(item['text']) > 60:
                    text += "..."
                print(f"    • {text}")
            
            if len(items) > 10:
                print(f"    ... and {len(items) - 10} more")
    
    print()
    print("=" * 80)
    print(f"📊 Summary: {total_count} untranslated strings in {len(all_findings)} files")
    print("=" * 80)
    print()
    print("💡 Recommendations:")
    print("  1. Wrap text content in {% trans %} tags")
    print("  2. Use {% trans %} for placeholder, title, and value attributes")
    print("  3. Run makemessages after fixing")
    print()


if __name__ == '__main__':
    main()

