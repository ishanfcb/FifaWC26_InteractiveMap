import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'mockData\s*=\s*\{.*?standings:\s*\[(.*?)\]\s*\}\s*;', text, re.DOTALL)
if match:
    teams = re.findall(r'name:\s*[\'\"](.*?)[\'\"].*?iso:\s*[\'\"](.*?)[\'\"]', match.group(1))
    for t, i in teams:
        if i not in ['un', 'us', 'mx', 'ca', 'br', 'ar', 'de', 'es', 'fr', 'gb-eng']:
            print(f'{t}: {i}')
