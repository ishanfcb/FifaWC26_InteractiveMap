import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

isos = re.findall(r'iso:\s*[\'\"](.*?)[\'\"]', text)
print(set(isos))
