import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Refined grouping logic:
# 1. Tickers with 'Z' or 'BADLAR' in name/notes -> Pesos BADLAR
# 2. Tickers with 'Y' -> Pesos TAMAR
# 3. Tickers with 'M' (except YM/TM/LM prefixes) -> Pesos Fijos
# 4. Tickers with 'D' -> USD MEP
# 5. Tickers with 'C' -> USD Cable
# 6. Tickers with 'O' or 'P' or 'L' -> Dólar Linked (including PNZCO)

def update_bond_properties(match):
    block = match.group(0)
    
    t_match = re.search(r'ticker:\s*"([^"]+)"', block)
    if not t_match:
        return block
    ticker = t_match.group(1)
    
    # Determine Group
    if ticker.startswith('PNZ') or ticker.endswith('O') or ticker.endswith('P') or ticker.endswith('L'):
        group = "Dólar Linked"
    elif ticker.endswith('D'):
        group = "USD MEP"
    elif ticker.endswith('C'):
        group = "USD Cable"
    elif ticker.endswith('Z'):
        group = "Pesos BADLAR"
    elif ticker.endswith('Y'):
        group = "Pesos TAMAR"
    elif ticker.endswith('M'):
        group = "Pesos Fijos"
    else:
        group = "Dólar Linked"

    block = re.sub(r'instrumentGroup:\s*"[^"]+"', f'instrumentGroup: "{group}"', block)
    return block

pattern = r'\{\s*id:\s*"bond_[^"]+".*?\n\s*\}'
new_content = re.sub(pattern, update_bond_properties, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Groups updated cleanly.")
