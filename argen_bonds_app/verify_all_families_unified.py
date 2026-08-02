import re
from collections import defaultdict

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

def get_base_stem(ticker):
    ticker = ticker.strip().upper()
    if len(ticker) >= 4 and ticker[-1] in ['D', 'C', 'O', 'Z', 'Y', 'P', 'L', 'M', 'A', 'B']:
        return ticker[:-1]
    return ticker

bonds_by_family = defaultdict(list)

pattern = r'\{\s*id:\s*"bond_([^"]+)".*?\n\s*\}'
matches = list(re.finditer(pattern, content, flags=re.DOTALL))

for m in matches:
    block = m.group(0)
    t_match = re.search(r'ticker:\s*"([^"]+)"', block)
    i_match = re.search(r'isin:\s*"([^"]+)"', block)
    if t_match and i_match:
        ticker = t_match.group(1)
        isin = i_match.group(1)
        stem = get_base_stem(ticker)
        bonds_by_family[stem].append((ticker, isin))

mismatches = []
total_bonds = 0

for stem, items in bonds_by_family.items():
    total_bonds += len(items)
    isins_in_family = set(item[1] for item in items)
    if len(isins_in_family) > 1:
        mismatches.append((stem, items))

print(f"Total Bond Families: {len(bonds_by_family)}")
print(f"Total Bonds Checked: {total_bonds}")
print(f"Total Families with ISIN Mismatches: {len(mismatches)}")

if len(mismatches) == 0:
    print("SUCCESS: 100% of all bond families share the EXACT SAME ISIN across all currency variants (D, C, O, Z, Y, M, A, B)!")
else:
    print("Mismatches found:", mismatches)
