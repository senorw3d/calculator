import re, json

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

isins = re.findall(r'isin:\s*"([^"]+)"', content)
lengths = set(len(i) for i in isins)
print(f"Total ISINs: {len(isins)}")
print(f"ISIN Lengths found: {lengths}")
print("Sample ISINs:", isins[:10])
