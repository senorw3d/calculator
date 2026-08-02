import re

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Filter out all SISTACO tickers ending in 'X' or 'Z'
removed_tickers = []
kept_count = 0

def filter_sistaco(match):
    global kept_count
    block = match.group(0)
    t_match = re.search(r'ticker:\s*"([^"]+)"', block)
    if t_match:
        ticker = t_match.group(1).upper()
        # If ends in X or Z (and length >= 4), remove it
        if len(ticker) >= 4 and (ticker.endswith('X') or ticker.endswith('Z')):
            removed_tickers.append(ticker)
            return '' # Remove from array
    kept_count += 1
    return block

pattern = r'\{\s*id:\s*"bond_[^"]+".*?\n\s*\},\s*'
new_content = re.sub(pattern, filter_sistaco, content, flags=re.DOTALL)

# Also clean up trailing commas if needed
new_content = re.sub(r',\s*\];', '\n];', new_content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Removed {len(removed_tickers)} SISTACO tickers (X/Z):", removed_tickers[:15], "...")
print(f"Kept {kept_count} retail bonds.")
