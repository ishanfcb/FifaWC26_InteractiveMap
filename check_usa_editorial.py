import re

with open('index.html', 'r', encoding='utf-8') as f: html = f.read()
editorial = re.search(r'const COUNTRY_EDITORIAL = \{.*?\};', html, re.DOTALL)
if editorial:
    usa = re.search(r'[\'\"]USA[\'\"]:\s*\{[^}]*\}', editorial.group(0))
    if usa: print('USA block in editorial:', usa.group(0))
