import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r'(\{\s*id:\s*"bond_YM34.*?\n\s*\})', content, flags=re.DOTALL)
for m in matches:
    print(m)
    print("="*60)
