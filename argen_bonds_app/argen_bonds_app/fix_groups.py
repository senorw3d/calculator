import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update instrumentGroup based on ticker endings:
# D = USD MEP
# C = USD Cable
# O, Z, Y, P, L = Dólar Linked
# M, A, B = Pesos (distributed into Pesos BADLAR, Pesos TAMAR, Pesos Fijos)

def fix_group(match):
    block = match.group(0)
    
    t_match = re.search(r'ticker:\s*"([^"]+)"', block)
    if not t_match:
        return block
    ticker = t_match.group(1)
    
    last_char = ticker[-1].upper()
    
    if last_char == 'D':
        group = "USD MEP"
    elif last_char == 'C':
        group = "USD Cable"
    elif last_char in ['O', 'Z', 'Y', 'P', 'L']:
        group = "Dólar Linked"
    elif last_char == 'M':
        group = "Pesos Fijos"
    elif last_char == 'A':
        group = "Pesos BADLAR"
    elif last_char == 'B':
        group = "Pesos TAMAR"
    else:
        group = "Dólar Linked"
        
    block = re.sub(r'instrumentGroup:\s*"[^"]+"', f'instrumentGroup: "{group}"', block)
    return block

pattern = r'\{\s*id:\s*"bond_[^"]+".*?\n\s*\}'
new_content = re.sub(pattern, fix_group, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated instrumentGroups based on ticker rules.")
