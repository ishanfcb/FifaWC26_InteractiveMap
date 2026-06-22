import re

with open('index.html', 'r', encoding='utf-8') as f: html = f.read()
m = re.search(r'async loadFallback\(\).*?table\s*=\s*\{\};(.*?)\} catch', html, re.DOTALL)
if m:
    with open('fallback_code.txt', 'w', encoding='utf-8') as out:
        out.write(m.group(1))
