import re

# 1. Update YM34 in data.js with EXACT terminal data:
# Ticker: YM34D / YM34C / YM34O
# CouponRate: 8.25
# CleanPrice: 110.23
# LastCouponDate: 2026-07-17
# Maturity: 2034-01-17

filepath_data = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath_data, 'r', encoding='utf-8') as f:
    content_data = f.read()

def update_ym34_exact(match):
    block = match.group(0)
    if 'ticker: "YM34D"' in block or 'ticker: "YM34C"' in block or 'ticker: "YM34O"' in block:
        block = re.sub(r'maturity:\s*"[^"]+"', 'maturity: "2034-01-17"', block)
        block = re.sub(r'couponRate:\s*[\d\.]+', 'couponRate: 8.25', block)
        block = re.sub(r'lastCouponDate:\s*"[^"]+"', 'lastCouponDate: "2026-07-17"', block)
        block = re.sub(r'cleanPrice:\s*[\d\.]+', 'cleanPrice: 110.23', block)
        block = re.sub(r'law:\s*"[^"]+"', 'law: "Nueva York"', block)
    return block

pattern = r'\{\s*id:\s*"bond_[^"]+".*?\n\s*\}'
new_content_data = re.sub(pattern, update_ym34_exact, content_data, flags=re.DOTALL)

with open(filepath_data, 'w', encoding='utf-8') as f:
    f.write(new_content_data)

print("Updated data.js with exact terminal data for YM34.")
