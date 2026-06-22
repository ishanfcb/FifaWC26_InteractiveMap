import json
import re

all_countries = {}
for i in range(1, 7):
    with open(f'batch{i}.json', 'r', encoding='utf-8') as f:
        all_countries.update(json.load(f))

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

cleaned_data = {}
for name, data in all_countries.items():
    pop_str = data.get('population', '')
    m = re.search(r'([\d,.]+)', pop_str)
    if m:
        pop = int(m.group(1).replace(',', '').replace('.', ''))
        if pop < 1000: # if it said 215 million, it might parse as 215
            if 'million' in pop_str.lower() or 'm' in pop_str.lower():
                pop *= 1000000
    else:
        pop = 'null'
        
    if name == 'Egypt': pop = 120000000
    if name == 'Brazil': pop = 215000000
    
    rank = rank_updates.get(name)
    if not rank:
        rank_str = str(data.get('rank', '0'))
        m_rank = re.search(r'(\d+)', rank_str)
        rank = int(m_rank.group(1)) if m_rank else 'null'
    if name == 'Algeria': rank = 28
    
    cleaned_data[name] = {'pop': pop, 'rank': rank}

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_country = None
for i, line in enumerate(lines):
    # Match "'CountryName': {" or '"CountryName": {'
    m = re.search(r'^\s*[\'\"]([^\'\"]+)[\'\"]:\s*\{', line)
    if m:
        current_country = m.group(1)
        continue
    
    if current_country and current_country in cleaned_data:
        if 'population:' in line and 'fifaRank:' not in line:
            lines[i] = re.sub(r'population:\s*[^,]+', f"population: {cleaned_data[current_country]['pop']}", line)
        elif 'fifaRank:' in line and 'population:' not in line:
            lines[i] = re.sub(r'fifaRank:\s*[^,]+', f"fifaRank: {cleaned_data[current_country]['rank']}", line)
        elif 'population:' in line and 'fifaRank:' in line:
            lines[i] = re.sub(r'population:\s*[^,]+', f"population: {cleaned_data[current_country]['pop']}", line)
            lines[i] = re.sub(r'fifaRank:\s*[^,]+', f"fifaRank: {cleaned_data[current_country]['rank']}", lines[i])

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Line-by-line data fix applied!")
