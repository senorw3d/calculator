import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'\{\s*id:\s*"bond_[^"]+".*?\n\s*\}'
matches = list(re.finditer(pattern, content, flags=re.DOTALL))

bonds = []
for m in matches:
    block = m.group(0)
    t = re.search(r'ticker:\s*"([^"]+)"', block)
    g = re.search(r'instrumentGroup:\s*"([^"]+)"', block)
    if t and g:
        bonds.append({'ticker': t.group(1), 'group': g.group(1)})

print(f"Total Bonds Loaded: {len(bonds)}")

tabs = ["USD MEP", "USD Cable", "Dólar Linked", "Pesos BADLAR", "Pesos TAMAR", "Pesos Fijos"]
for tab in tabs:
    count = sum(1 for b in bonds if b['group'] == tab)
    print(f"Tab '{tab}': {count} bonds")
