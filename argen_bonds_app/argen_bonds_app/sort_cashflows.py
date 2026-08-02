import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# For every cashFlows: [ ... ], sort the objects by date
def sort_cf_block(match):
    prefix = match.group(1)
    cf_body = match.group(2)
    
    # Parse individual { ... } items
    items = re.findall(r'\{\s*date:\s*"([^"]+)",\s*amortization:\s*([\d\.]+),\s*coupon:\s*([\d\.]+),\s*amount:\s*([\d\.]+),\s*residual:\s*([\d\.]+)\s*\}', cf_body)
    
    # Sort by date (YYYY-MM-DD string sorting works fine)
    items_sorted = sorted(items, key=lambda x: x[0])
    
    # Reconstruct
    formatted_items = [
        f'{{ date: "{d}", amortization: {a}, coupon: {c}, amount: {am}, residual: {r} }}'
        for d, a, c, am, r in items_sorted
    ]
    
    return prefix + "[\n        " + ",\n        ".join(formatted_items) + "\n      ]"

pattern = r'(cashFlows:\s*)(\[\s*\{.*?\}\s*\])'
new_content = re.sub(pattern, sort_cf_block, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully sorted all cashflows chronologically.")
