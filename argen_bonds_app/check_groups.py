import re
from collections import Counter

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

groups = re.findall(r'instrumentGroup:\s*"([^"]+)"', content)
print("Group breakdown:", Counter(groups))
