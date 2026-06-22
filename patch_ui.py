import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update fmtPop
new_fmt_pop = """function fmtPop(n) {
            if (!n || n === 'null') return '—';
            // Assuming n is a pure integer representing headcount.
            if (n >= 1e9) return (n / 1e9).toFixed(1) + 'B';
            if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
            return n.toLocaleString();
        }"""
text = re.sub(r'function\s+fmtPop\(n\)\s*\{[^\}]+\}', new_fmt_pop, text)

# 2. Add Timeline Expansion CSS
if '.ic-timeline-card.expanded' not in text:
    css_addition = """
        .ic-timeline-card {
            cursor: pointer;
            transition: max-height 0.2s ease, padding 0.2s ease;
            max-height: 4.5em; /* roughly two lines */
            overflow: hidden;
            position: relative;
        }
        .ic-timeline-card.expanded {
            max-height: 500px;
        }
        .ic-timeline-card::after {
            content: '▼';
            position: absolute;
            bottom: 8px;
            right: 8px;
            font-size: 10px;
            color: rgba(255, 255, 255, 0.4);
            transition: transform 0.2s ease;
        }
        .ic-timeline-card.expanded::after {
            transform: rotate(180deg);
        }
"""
    text = text.replace('</style>', css_addition + '\n    </style>')

# 3. Add JS toggle for timeline cards
# In renderInfoTimeline, add the click listener
new_timeline_js = """function renderInfoTimeline(entries, container, accentColor) {
            if (!entries || !entries.length) return;
            entries.forEach((entry, i) => {
                const card = el('div', 'ic-timeline-card');
                const yr = el('div', 'ic-timeline-year'); yr.textContent = entry.year;
                const ev = el('div', 'ic-timeline-event'); ev.textContent = entry.event;
                card.appendChild(yr); card.appendChild(ev);
                card.addEventListener('click', () => card.classList.toggle('expanded'));
                container.appendChild(card);
            });
        }"""
text = re.sub(r'function\s+renderInfoTimeline\(.*?\)\s*\{(?:[^{}]*|\{[^{}]*\})*\}', new_timeline_js, text, flags=re.DOTALL)


# 4. Fix Flag ISO code to lowercase 2-letter
text = re.sub(r'\`https://flagcdn\.com/w320/\$\{\s*iso\s*}\.png\`', 
              r'`https://flagcdn.com/w320/${(iso || "un").slice(0, 2).toLowerCase()}.png`', text)

# 5. Fix FIFA Rank Rendering and Guard
rank_render_replacement = """
            let rankStr = null;
            if (ed.fifaRank !== null && ed.fifaRank !== undefined && ed.fifaRank !== 'null') {
                const parsedRank = parseInt(ed.fifaRank, 10);
                if (parsedRank > 300 || !isFinite(parsedRank) || isNaN(parsedRank)) {
                    console.warn(`Invalid FIFA rank for ${countryName}:`, ed.fifaRank);
                    rankStr = '—';
                } else {
                    rankStr = `#${Math.round(parsedRank)}`;
                }
            }
            statsRow.appendChild(makeTile('FIFA Rank', rankStr, ''));
"""
text = re.sub(r'statsRow\.appendChild\(makeTile\(\'FIFA Rank\',\s*ed\.fifaRank[^)]+\)\);', rank_render_replacement.strip(), text)


# 6. Overview coming soon fallback
overview_replacement = """
            const ovHead = el('div', 'ic-section-heading'); ovHead.textContent = 'Footballing Overview';
            const ovText = el('p', 'ic-overview'); 
            ovText.textContent = ed.overview && ed.overview.trim() ? ed.overview : 'Overview coming soon.';
            body.appendChild(ovHead); body.appendChild(ovText);
"""
text = re.sub(r'const ovHead = el\(\'div\', \'ic-section-heading\'\).*?body\.appendChild\(ovText\);', overview_replacement.strip(), text, flags=re.DOTALL)

# 7. Add console.log to map click handler
click_log_replacement = """function countryClick(event, d, countryElement, specificTeamName = null) {
            console.log("Map Click: countryId =", d.properties.name, specificTeamName);
            if (event && event.stopPropagation) event.stopPropagation();
"""
text = re.sub(r'function countryClick\(event, d, countryElement, specificTeamName = null\)\s*\{\s*if\s*\(event\s*&&\s*event\.stopPropagation\)\s*event\.stopPropagation\(\);', click_log_replacement, text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("UI patches applied!")
