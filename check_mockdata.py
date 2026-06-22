import re

with open('index.html', 'r', encoding='utf-8') as f: html = f.read()
standings = re.search(r'const mockData = \{.*?standings:\s*\[(.*?)\]\s*\}\s*;', html, re.DOTALL)
if standings:
    print('Found standings.')
    usa = re.search(r'\{.*?name:\s*[\'\"]USA[\'\"].*?\}', standings.group(1), re.DOTALL)
    if usa: print('USA in mockData:', usa.group(0))
