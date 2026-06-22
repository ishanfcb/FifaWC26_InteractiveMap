import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('script_dump.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find fmtPop or population formatting
pop_fmt = re.search(r'function\s+fmtPop.*?\{.*?\}', text, re.DOTALL)
if pop_fmt: print('Found pop_fmt:', pop_fmt.group(0))

# Find the country card rendering function
render = re.search(r'function\s+renderCountryCard.*?\{.*?(?=\nfunction)', text, re.DOTALL)
if render: print('\nFound renderCountryCard:\n', render.group(0))

click = re.search(r'\.on\([\'\"]click[\'\"].*?\}', text, re.DOTALL)
if click: print('\nFound click logic:\n', click.group(0)[:500])

# Timeline extraction
timeline = re.search(r'const\s+timelineCard\s*=\s*document\.createElement.*?\}', text, re.DOTALL)
if timeline: print('\nFound timeline:\n', timeline.group(0))

with open('debug_output.txt', 'w', encoding='utf-8') as f:
    if pop_fmt: f.write(pop_fmt.group(0) + '\n\n')
    if render: f.write(render.group(0) + '\n\n')
