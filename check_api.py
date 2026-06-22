import re
with open('script_dump.js', 'r', encoding='utf-8') as f: text = f.read()
primary = re.search(r'PRIMARY\s*=\s*[\'\"](.*?)[\'\"]', text)
if primary: print('PRIMARY API:', primary.group(1))
