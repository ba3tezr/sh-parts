import re

files = ['cars/views.py', 'inventory/views.py', 'customers/views.py', 'sales/views.py']

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add import if not exists
        if 'IsAuthenticatedOrReadOnly' not in content:
            content = content.replace(
                'from rest_framework.response import Response',
                'from rest_framework.response import Response\nfrom rest_framework.permissions import IsAuthenticatedOrReadOnly'
            )
        
        # Find all ViewSet classes and add permission_classes if not exists
        lines = content.split('\n')
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            # If this is a ViewSet class definition
            if re.match(r'^class \w+ViewSet\(', line):
                # Check if permission_classes already exists in next few lines
                has_permission = False
                for j in range(i+1, min(i+5, len(lines))):
                    if 'permission_classes' in lines[j]:
                        has_permission = True
                        break
                
                # Add permission_classes if not exists
                if not has_permission:
                    # Get indentation from next line
                    next_line_indent = len(lines[i+1]) - len(lines[i+1].lstrip()) if i+1 < len(lines) else 4
                    new_lines.append(' ' * next_line_indent + 'permission_classes = [IsAuthenticatedOrReadOnly]')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✅ Updated {filepath}")
    except Exception as e:
        print(f"❌ Error in {filepath}: {e}")
