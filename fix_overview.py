import json
import re

# Load all batches
all_countries = {}
for i in range(1, 7):
    with open(f'batch{i}.json', 'r', encoding='utf-8') as f:
        all_countries.update(json.load(f))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for name, data in all_countries.items():
    overview = data.get('overview', '')
    # escape backticks since it's injected into a template literal
    overview = overview.replace('`', '\\`')
    
    # We want to replace overview: `...`,
    # But wait, in html it's `overview: \`\`,`
    
    pattern = r"('" + re.escape(name) + r"':\s*\{.*?overview:\s*)`[^`]*`"
    html = re.sub(pattern, rf"\g<1>`{overview}`", html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Overviews injected!")
