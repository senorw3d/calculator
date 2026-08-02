filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'rb') as f:
    raw = f.read()

# Replace corrupted bytes sequence for Dólar Linked with correct UTF-8
# \xc3\x83\xc2\xb3 or \xc3\xb3
text = raw.decode('utf-8', errors='ignore')
text = text.replace('Dlar Linked', 'Dólar Linked')
text = text.replace('DÃ³lar Linked', 'Dólar Linked')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved clean UTF-8 data.js")
