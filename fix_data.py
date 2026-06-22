import json
import re
import glob

# Load all batches
all_countries = {}
for i in range(1, 7):
    with open(f'batch{i}.json', 'r', encoding='utf-8') as f:
        all_countries.update(json.load(f))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Rank overrides from earlier
rank_updates = {
    'Bosnia and Herzegovina': 64, 'DR Congo': 43, "Côte d'Ivoire": 30,
    'Curaçao': 83, 'Czechia': 40, 'Ecuador': 23, 'Egypt': 29,
    'France': 3, 'Ghana': 65, 'IR Iran': 20, 'Iraq': 57,
    'Japan': 18, 'Jordan': 63, 'Korea Republic': 25, 'Mexico': 14,
    'Morocco': 6, 'Netherlands': 8, 'New Zealand': 85, 'Norway': 31,
    'Panama': 34, 'Paraguay': 41, 'Portugal': 5, 'Qatar': 56,
    'Saudi Arabia': 61, 'Scotland': 42, 'Senegal': 15, 'South Africa': 60,
    'Spain': 2, 'Sweden': 38, 'Tunisia': 45, 'Türkiye': 22,
    'Uruguay': 16, 'USA': 17, 'Uzbekistan': 50
}

# Fix populations and ranks
for name, data in all_countries.items():
    pop_str = data.get('population', '')
    m = re.match(r'^[\d,.]+', pop_str.strip())
    if m:
        pop_clean = m.group(0).replace(',', '').replace('.', '')
        if name == 'Egypt':
            pop = 120000000
        else:
            pop = int(pop_clean)
    else:
        pop = 'null'
        
    rank = rank_updates.get(name)
    if not rank:
        rank_str = data.get('rank', '0')
        m_rank = re.match(r'^#?(\d+)', rank_str.strip())
        rank = int(m_rank.group(1)) if m_rank else 'null'
        
    # Now find the country block in HTML and replace population and fifaRank
    pattern = r"('" + re.escape(name) + r"':\s*\{.*?population:\s*)(\d+|null)(.*?fifaRank:\s*)(\d+|null)"
    
    html = re.sub(pattern, rf"\g<1>{pop}\g<3>{rank}", html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Data fixed in index.html!")
