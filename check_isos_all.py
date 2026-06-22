import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'mockData\s*=\s*\{.*?standings:\s*\[(.*?)\]\s*\}\s*;', text, re.DOTALL)
if match:
    isos = re.findall(r'iso:\s*[\'\"](.*?)[\'\"]', match.group(1))
    print('ISOs in mockData:', set(isos))
else:
    print('Not found')
