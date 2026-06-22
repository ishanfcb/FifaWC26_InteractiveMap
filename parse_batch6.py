import re, json

with open('The 6 fields.txt', 'r', encoding='utf-8') as f:
    text = f.read()

countries = re.split(r'\n---\n+', text)
parsed = {}
# Batch 6: indices 41 to 49
for c in countries[41:49]:
    lines = [line.strip() for line in c.strip().split('\n') if line.strip()]
    if not lines: continue
    name = lines[0].strip('* ')
    data = {'name': name}
    
    full_text = '\n'.join(lines[1:])
    
    # extract population
    pop_match = re.search(r'\*\*population:\*\*\s*(.+)', full_text, re.IGNORECASE)
    if pop_match: data['population'] = pop_match.group(1).strip()
    
    # extract rank
    rank_match = re.search(r'\*\*Fifa Rank.*?\*\*\s*(.*?)(?:\n|$)', full_text, re.IGNORECASE)
    if rank_match: data['rank'] = rank_match.group(1).strip()
    
    # extract overview
    overview_match = re.search(r'\*\*Footballing [Oo]verview.*?\*\*\s*(.+)', full_text)
    if overview_match: data['overview'] = overview_match.group(1).strip()
    
    # extract rivals
    rivals_match = re.search(r'\*\*rivals.*?\*\*\s*(.*?)(?=\n- \*\*|$)', full_text, re.IGNORECASE | re.DOTALL)
    if rivals_match: data['rivals'] = rivals_match.group(1).strip()
    
    # extract history
    hist_match = re.search(r'\*\*Footballing [Hh]istory.*?:\*\*(.*?)(?=\n- \*\*watch out for|$)', full_text, re.IGNORECASE | re.DOTALL)
    if not hist_match:
        hist_match = re.search(r'- Footballing \+ political history:(.*?)(?=\n- \*\*watch out for|$)', full_text, re.IGNORECASE | re.DOTALL)
    if hist_match: 
        hist_text = hist_match.group(1).strip()
        timeline = []
        for line in hist_text.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                parts = re.split(r':|—| - ', line[2:], 1)
                if len(parts) == 2:
                    timeline.append({'year': parts[0].strip(' *'), 'event': parts[1].strip(' *')})
        data['timeline'] = timeline
        
    # watch out for
    watch_match = re.search(r'\*\*watch out for.*?\*\*(.*?)$', full_text, re.IGNORECASE | re.DOTALL)
    if watch_match:
        watch_text = watch_match.group(1).strip()
        players = []
        for line in watch_text.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                parts = re.split(r' — | - ', line[2:], 1)
                if len(parts) == 2:
                    players.append({'name': parts[0].strip(), 'club': parts[1].strip()})
        data['players'] = players

    parsed[name] = data

with open('batch6.json', 'w', encoding='utf-8') as f:
    json.dump(parsed, f, indent=2)
