import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Specifically update YM34 (YM34D, YM34C, YM34O) with exact official specs:
# Maturity: 2034-01-15
# CouponRate: 9.50
# CleanPrice: 110.60 for YM34D / 110.60 for YM34C / 108.50 for YM34O
# Law: Nueva York
def update_ym34(match):
    block = match.group(0)
    if 'ticker: "YM34D"' in block or 'ticker: "YM34C"' in block or 'ticker: "YM34O"' in block:
        block = re.sub(r'maturity:\s*"[^"]+"', 'maturity: "2034-01-15"', block)
        block = re.sub(r'couponRate:\s*[\d\.]+', 'couponRate: 9.50', block)
        block = re.sub(r'lastCouponDate:\s*"[^"]+"', 'lastCouponDate: "2026-01-15"', block)
        block = re.sub(r'law:\s*"[^"]+"', 'law: "Nueva York"', block)
        if 'YM34D' in block:
            block = re.sub(r'cleanPrice:\s*[\d\.]+', 'cleanPrice: 110.60', block)
        elif 'YM34C' in block:
            block = re.sub(r'cleanPrice:\s*[\d\.]+', 'cleanPrice: 110.60', block)
        else:
            block = re.sub(r'cleanPrice:\s*[\d\.]+', 'cleanPrice: 108.50', block)
    return block

pattern = r'\{\s*id:\s*"bond_[^"]+".*?\n\s*\}'
new_content = re.sub(pattern, update_ym34, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated YM34 in data.js with official prospectus data.")
