import re

with open('index.html', 'r', encoding='utf-8') as f: html = f.read()

# Add USA to OF_NAME_MAP
html = re.sub(r"'United States':\s*'USA',", r"'United States': 'USA', 'USA': 'USA',", html)

# Add USA to OF_ISO_MAP
html = re.sub(r"'United States':'us',", r"'United States':'us','USA':'us',", html)

# Add USA to OF_MAPNAME
html = re.sub(r"'United States':'United States of America',", r"'United States':'United States of America','USA':'United States of America',", html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Fallback fixed!")
