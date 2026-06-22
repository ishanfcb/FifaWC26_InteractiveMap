import json
import re

with open('batch6.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update specific ranks based on web search
rank_updates = {
    'Spain': 2,
    'Sweden': 38,
    'Switzerland': 19,
    'Tunisia': 45,
    'Türkiye': 22,
    'Uruguay': 16,
    'USA': 17,
    'Uzbekistan': 50
}

wc_won_updates = {
    'Spain': 1,
    'Uruguay': 2
}

new_countries = []
for name, data in batch.items():
    
    # Clean up population string to int
    pop_str = data.get('population', '0')
    pop_clean = re.sub(r'[^0-9]', '', pop_str)
    pop = int(pop_clean) if pop_clean else 'null'
    
    # Clean up rank string to int
    if name in rank_updates:
        rank = rank_updates[name]
    else:
        rank_str = data.get('rank', '0')
        rank_clean = re.sub(r'[^0-9]', '', rank_str)
        rank = int(rank_clean) if rank_clean else 'null'
        
    wc_won = wc_won_updates.get(name, 0)
    
    overview = data.get('overview', '').replace('`', '\\`')
    rivals = data.get('rivals', '').replace('`', '\\`')
    
    timeline_str = '[\n'
    for item in data.get('timeline', []):
        year = item.get('year', '').replace('`', '\\`')
        event = item.get('event', '').replace('`', '\\`')
        timeline_str += f"                    {{ year: `{year}`, event: `{event}` }},\n"
    timeline_str += '                ]'
    
    players_str = '[\n'
    for item in data.get('players', []):
        pname = item.get('name', '').replace('`', '\\`')
        club = item.get('club', '').replace('`', '\\`')
        players_str += f"                    {{ name: `{pname}`, club: `{club}` }},\n"
    players_str += '                ]'
    
    country_obj = f"""
            '{name}': {{
                continent: '—', language: '—',
                population: {pop},
                fifaRank: {rank},
                wcWon: {wc_won},
                rivals: `{rivals}`,
                overview: `{overview}`,
                timeline: {timeline_str},
                form: [], // TODO: Source from live API
                players: {players_str}
            }},"""
    new_countries.append(country_obj)

# This is the last batch, we can remove the placeholder or keep it
injection = ''.join(new_countries)

html = html.replace('// Add more countries here when data is ready', injection)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
