import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

dl_matches = re.findall(r'instrumentGroup:\s*"Dólar Linked"', content)
print(f"Exact matches for 'Dólar Linked': {len(dl_matches)}")

mep_matches = re.findall(r'instrumentGroup:\s*"USD MEP"', content)
print(f"Exact matches for 'USD MEP': {len(mep_matches)}")

ccl_matches = re.findall(r'instrumentGroup:\s*"USD Cable"', content)
print(f"Exact matches for 'USD Cable': {len(ccl_matches)}")
