# FIFA World Cup 2026 Interactive Map

An interactive, responsive client-side world map visualization showcasing the FIFA World Cup 2026 teams, standings, schedule, and live match updates.

## Data Flow & Architecture

The application is structured as a single-page client-side web application. It retrieves and renders World Cup match data entirely at runtime in the client's browser, eliminating the need for periodic rebuilds or site redeployments:

1. **Primary Live Data Fetch (Runtime/Client-side):**
   - On map initialization and periodic intervals (every 10 minutes, or 60 seconds during live games), the client-side D3 service queries the live API:
     - `https://worldcup26.ir/get/teams`
     - `https://worldcup26.ir/get/groups`
     - `https://worldcup26.ir/get/games`
   - Requests are routed securely over HTTPS to avoid Mixed Content security blocks in modern browsers.
   - Any updates in the live database are instantly rendered in the browser for visitors in real-time.

2. **Automatic Offline Fallback:**
   - If the primary API is unreachable, the system automatically falls back to fetching match results from the public openfootball repository:
     - `https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json`
   - Standings and statistics are then dynamically re-calculated in the client's browser using these match scores.

## Main Map Features

- **Smart Camera Centering:** For countries with overseas territories or multi-island groups (e.g., Spain, Portugal, USA, France, Netherlands), the map's zoom-to-country functionality automatically calculates the largest single polygon by area (the mainland) to center and scale the viewport, avoiding zoom focus on minor offshore islands.
