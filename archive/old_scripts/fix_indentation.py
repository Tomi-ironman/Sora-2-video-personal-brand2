#!/usr/bin/env python3
"""
Quick script to fix indentation issues in market_intelligence_web.py
"""

def fix_indentation():
    with open('market_intelligence_web.py', 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    in_try_block = False
    
    for i, line in enumerate(lines):
        # Fix common indentation patterns
        if line.strip().startswith('try:') and not line.startswith('    try:'):
            in_try_block = True
            fixed_lines.append(line)
        elif in_try_block and line.strip() and not line.startswith('    ') and not line.startswith('except') and not line.startswith('def ') and not line.startswith('@'):
            # Add proper indentation for lines inside try blocks
            fixed_lines.append('    ' + line)
        elif line.strip().startswith('except') or line.strip().startswith('finally'):
            in_try_block = False
            fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    with open('market_intelligence_web.py', 'w') as f:
        f.writelines(fixed_lines)
    
    print("✅ Fixed indentation issues")

if __name__ == "__main__":
    fix_indentation()
