import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

usa = re.search(r'[\'\"]USA[\'\"]:\s*\{[^}]*\}', html)
if usa:
    print('USA block:', usa.group(0))
