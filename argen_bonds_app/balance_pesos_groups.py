import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update Pesos groups nicely
def update_pesos_distribution(match):
    block = match.group(0)
    t_match = re.search(r'ticker:\s*"([^"]+)"', block)
    if not t_match:
        return block
    ticker = t_match.group(1).upper()
    
    if ticker.endswith('A'):
        block = re.sub(r'instrumentGroup:\s*"[^"]+"', 'instrumentGroup: "Pesos BADLAR"', block)
    elif ticker.endswith('B'):
        block = re.sub(r'instrumentGroup:\s*"[^"]+"', 'instrumentGroup: "Pesos TAMAR"', block)
    elif ticker.endswith('M'):
        block = re.sub(r'instrumentGroup:\s*"[^"]+"', 'instrumentGroup: "Pesos Fijos"', block)
        
    return block

pattern = r'\{\s*id:\s*"bond_[^"]+".*?\n\s*\}'
new_content = re.sub(pattern, update_pesos_distribution, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated Pesos tabs distribution.")
