function countryClick(event, d, countryElement, specificTeamName = null) {
            if (event && event.stopPropagation) event.stopPropagation(); 
            const mapName = d.properties.name;
            const countryData = specificTeamName ? findTeamStandingsData(specificTeamName, true) : findTeamStandingsData(mapName);

            if (countryData) {
                const element = countryElement || d3.select(this);
                setActiveCountry(element, d);
                openCountryDetail(countryData.team.name, countryData);
                highlightStandingsRow(countryData.team.name);
                
                const bounds = path.bounds(d);
                const dx = bounds[1][0] - bounds[0][0];
                const dy = bounds[1][1] - bounds[0][1];
                const x = (bounds[0][0] + bounds[1][0]) / 2;
                const y = (bounds[0][1] + bounds[1][1]) / 2;
                
                const scale = Math.max(1.5, Math.min(5, 0.20 / Math.max(dx / window.innerWidth, dy / window.innerHeight)));
                const targetX = window.innerWidth / 2;
                const targetY = (window.innerHeight - 240) / 2;

                const translate = [targetX - scale * x, targetY - scale * y];

                svg.transition()
                    .duration(750)
                    .call(zoom.transform, d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale));
            }