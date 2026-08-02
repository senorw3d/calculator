import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'rb') as f:
    raw = f.read()

# Replace any mangled/corrupted sequence for Dólar Linked with clean UTF-8
text = raw.decode('utf-8', errors='ignore')
text = re.sub(r'D[^\w\s]?lar Linked', 'Dólar Linked', text)
text = text.replace('Dlar Linked', 'Dólar Linked')
text = text.replace('DÃ³lar Linked', 'Dólar Linked')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed encoding in data.js!")
