import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'standings:\s*\[.*?\]', text, re.DOTALL)
if match:
    isos = re.findall(r'iso:\s*[\'\"](.*?)[\'\"]', match.group(0))
    print('ISOs:', set(isos))
