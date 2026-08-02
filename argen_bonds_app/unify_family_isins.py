import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Group bonds by base ticker stem (e.g., YM34D, YM34C, YM34O -> YM34)
# Assign the exact same ISIN to all currency variants of the same bond family!

def get_base_stem(ticker):
    # Strip single trailing currency indicator D, C, O, Z, Y, P, L, M, A, B if length > 3
    if len(ticker) >= 4 and ticker[-1] in ['D', 'C', 'O', 'Z', 'Y', 'P', 'L', 'M', 'A', 'B']:
        return ticker[:-1]
    return ticker

# Build dictionary of stem -> master ISIN
stem_isin_map = {}

# Parse all bonds
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
        
        # Priority for known international/official ISINs or first found ISIN for the family
        if stem not in stem_isin_map or isin.startswith("USP") or isin.startswith("US"):
            stem_isin_map[stem] = isin

print(f"Mapped {len(stem_isin_map)} bond families. Sample mappings:")
for k, v in list(stem_isin_map.items())[:15]:
    print(f"  Base Family '{k}': ISIN = '{v}'")

def unify_family_isin(match):
    block = match.group(0)
    t_match = re.search(r'ticker:\s*"([^"]+)"', block)
    if t_match:
        ticker = t_match.group(1)
        stem = get_base_stem(ticker)
        master_isin = stem_isin_map.get(stem, "AR000" + ticker)
        block = re.sub(r'isin:\s*"[^"]+"', f'isin: "{master_isin}"', block)
    return block

new_content = re.sub(pattern, unify_family_isin, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Unified ISINs across all currency variants (D, C, O, Z, Y).")
