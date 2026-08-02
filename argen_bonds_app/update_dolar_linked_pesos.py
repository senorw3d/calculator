import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update currency and paymentCurrency for O, P, L, M, A, B tickers to ARS
def update_currency_and_group(match):
    block = match.group(0)
    t_match = re.search(r'ticker:\s*"([^"]+)"', block)
    if not t_match:
        return block
    ticker = t_match.group(1).upper()
    last_char = ticker[-1]
    
    if last_char in ['O', 'P', 'L', 'M', 'A', 'B']:
        block = re.sub(r'currency:\s*"[^"]+"', 'currency: "ARS"', block)
        block = re.sub(r'paymentCurrency:\s*"[^"]+"', 'paymentCurrency: "ARS"', block)
    elif last_char == 'D' or last_char == 'C':
        block = re.sub(r'currency:\s*"[^"]+"', 'currency: "USD"', block)
        block = re.sub(r'paymentCurrency:\s*"[^"]+"', 'paymentCurrency: "USD"', block)
        
    return block

pattern = r'\{\s*id:\s*"bond_[^"]+".*?\n\s*\}'
new_content = re.sub(pattern, update_currency_and_group, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated currency and paymentCurrency for Pesos/DL tickers.")
