import json
import re

with open('batch1.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add rivals to Argentina
arg_rivals = batch['Argentina'].get('rivals', '').replace('"', '\\"')
arg_pattern = r"('Argentina': \{.*?overview: `.*?`,)"
arg_repl = r"\1\n                rivals: `" + arg_rivals + r"`,"
html = re.sub(arg_pattern, arg_repl, html, flags=re.DOTALL)

# Format the new countries
new_countries = []
for name, data in batch.items():
    if name == 'Argentina': continue
    
    # Clean up population string to int
    pop_str = data.get('population', '0')
    pop_clean = re.sub(r'[^0-9]', '', pop_str)
    pop = int(pop_clean) if pop_clean else 'null'
    
    # Clean up rank string to int
    rank_str = data.get('rank', '0')
    rank_clean = re.sub(r'[^0-9]', '', rank_str)
    rank = int(rank_clean) if rank_clean else 'null'
    
    # wcWon based on search results
    wc_won = 0
    if name == 'Brazil': wc_won = 5
    
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

injection = ''.join(new_countries) + '\n            // Add more countries here when data is ready'

html = html.replace('// Add more countries here when data is ready', injection)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
