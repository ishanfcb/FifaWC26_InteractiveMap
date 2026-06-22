import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

click_match = re.search(r'function countryClick\(.*?\}', text, re.DOTALL)
if click_match:
    with open('click_func.js', 'w', encoding='utf-8') as f:
        f.write(click_match.group(0))

render_match = re.search(r'function renderCountryCard\(.*?\n\}', text, re.DOTALL)
if not render_match:
    render_match = re.search(r'function openCountryDetail\(.*?(?=\n\s+function|\n\s+//)', text, re.DOTALL)
if render_match:
    with open('render_func.js', 'w', encoding='utf-8') as f:
        f.write(render_match.group(0))

empty = []
for m in re.finditer(r'\'(.*?)\':\s*\{\s*continent:.*?overview:\s*`([^`]*)`', text, re.DOTALL):
    if not m.group(2).strip():
        empty.append(m.group(1))
with open('empty_overviews.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(empty))
