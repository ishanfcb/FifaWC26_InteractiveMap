import re
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

empty_overview = []
for m in re.finditer(r'\'(.*?)\':\s*\{\s*continent:.*?overview:\s*`([^`]*)`', text, re.DOTALL):
    if not m.group(2).strip():
        empty_overview.append(m.group(1))

print("Empty overviews:", empty_overview)

click = re.search(r'function countryClick\(.*?\n\}', text, re.DOTALL)
if click: print(click.group(0)[:300])

click_event = re.search(r'd3\.select\(.*?\.on\("click".*?\}', text, re.DOTALL)
if click_event: print(click_event.group(0)[:500])

flag = re.search(r'https://flagcdn\.com/.*?\`', text)
if flag: print(flag.group(0))

