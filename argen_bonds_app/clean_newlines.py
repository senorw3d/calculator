import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove multiple blank lines
clean_content = re.sub(r'\n\s*\n', '\n', content)
clean_content = re.sub(r'^\s+$', '', clean_content, flags=re.MULTILINE)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(clean_content)

print(f"Cleaned up data.js. Length is now {len(clean_content)} characters.")
