import re
with open('index.html', 'r', encoding='utf-8') as f: html = f.read()

# Replace all `${...iso...}.png` with `${(...iso...).slice(0, 2).toLowerCase()}.png`
# But only if it's not already .slice(0, 2)
def replacer(match):
    var = match.group(1)
    if '.slice(' in var: return match.group(0)
    return f"`https://flagcdn.com/w40/${{({var} || 'un').slice(0, 2).toLowerCase()}}.png`"

html = re.sub(r'`https://flagcdn\.com/w40/\$\{([^}]+)\}\.png`', replacer, html)

# And for the <img src="...">
html = re.sub(r'src="https://flagcdn\.com/w40/\$\{([^}]+)\}\.png"', 
              lambda m: f'src="https://flagcdn.com/w40/${{({m.group(1)} || \'un\').slice(0, 2).toLowerCase()}}.png"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
