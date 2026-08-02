import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

matches = [m.start() for m in re.finditer(r'ticker:\s*"TTCED"', content)]
print("TTCED positions:", matches)
for m in matches:
    print(content[m-50:m+400])
    print("="*50)
