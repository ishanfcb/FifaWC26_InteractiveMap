import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def check(country):
    m = re.search(r'[\'\"]' + country + r'[\'\"]:\s*\{.*?population:\s*(.*?),\s*fifaRank:\s*(.*?),', html, re.DOTALL)
    if m:
        print(f"{country}: Population={m.group(1).strip()}, FIFA Rank={m.group(2).strip()}")
    else:
        print(f"{country} not found")

check("Egypt")
check("Brazil")
check("Algeria")
check("USA")
