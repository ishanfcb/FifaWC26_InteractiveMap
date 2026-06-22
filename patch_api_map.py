import re
with open('index.html', 'r', encoding='utf-8') as f: html = f.read()

# Add more US variations to API_TO_MAP_NAME just in case
more_maps = """
            'United States': 'United States of America',
            'USA': 'United States of America',
            'US': 'United States of America',
            'U.S.': 'United States of America',
            'U.S.A.': 'United States of America',
            'United States of America': 'United States of America',
"""
html = re.sub(r"'United States':\s*'United States of America',\s*'USA':\s*'United States of America',", more_maps, html)

with open('index.html', 'w', encoding='utf-8') as f: f.write(html)
print("Updated API_TO_MAP_NAME")
