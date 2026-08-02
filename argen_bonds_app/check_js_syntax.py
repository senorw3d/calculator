import re
import json

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Strip export const
js_array = content[content.find('['):content.rfind(']')+1]

# Quote keys
js_array = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)(\s*:)', r'\1"\2"\3', js_array)

# Handle trailing commas
js_array = re.sub(r',\s*([\]}])', r'\1', js_array)

try:
    data = json.loads(js_array)
    print("Parsed successfully!", len(data), "items")
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
    lines = js_array.split('\n')
    line_num = e.lineno - 1
    print("Error around line:")
    for i in range(max(0, line_num-5), min(len(lines), line_num+5)):
        print(f"{i}: {lines[i]}")
