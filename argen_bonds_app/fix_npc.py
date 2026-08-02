import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

def fix_npc_issuer(match):
    block = match.group(0)
    t_match = re.search(r'ticker:\s*"([^"]+)"', block)
    if t_match:
        ticker = t_match.group(1)
        if ticker.startswith('NPC'):
            block = re.sub(r'issuer:\s*"[^"]+"', 'issuer: "Central Puerto S.A."', block)
            block = re.sub(r'shortIssuer:\s*"[^"]+"', 'shortIssuer: "Central Puerto"', block)
    return block

pattern = r'\{\s*id:\s*"bond_[^"]+".*?\n\s*\}'
new_content = re.sub(pattern, fix_npc_issuer, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated NPC to Central Puerto S.A.")
