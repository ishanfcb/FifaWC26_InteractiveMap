function openCountryDetail(countryName, countryData) {
            const rightPanel = d3.select('#right-panel');
            const content = document.getElementById('country-detail-content');
            content.innerHTML = '';

            const iso = countryData.team.iso;
            const groupColor = (() => {
                for (const g of mockData.standings)
                    if (g.teams.some(t => t.name === countryName)) return g.color;
                return '#888';
            })();
            const ed = getEditorial(countryName, iso);