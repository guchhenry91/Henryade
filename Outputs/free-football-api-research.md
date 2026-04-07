# Free Football/Soccer APIs with Player-Level Stats (xG, Shots, Assists)

Research date: 5 April 2026

---

## QUICK VERDICT

| Source | Free? | Player Stats? | xG? | Shots? | EPL/LaLiga/UCL? | API (not scraping)? | Browser CORS? | Recommendation |
|--------|-------|--------------|-----|--------|-----------------|--------------------|--------------:|----------------|
| **FotMob (internal API)** | Yes | Yes | Yes | Yes | Yes/Yes/Yes | Unofficial REST | No (needs proxy) | **BEST OPTION** |
| **Understat** | Yes | Yes | Yes | Yes | Yes/Yes/No UCL | Scraping (embedded JSON) | No (needs proxy) | **TOP PICK for xG** |
| **API-Football** | Freemium (100 req/day) | Yes | Limited | Yes | Yes/Yes/Yes | Official REST | Yes (with key) | **BEST OFFICIAL API** |
| **StatsBomb Open Data** | Yes | Yes | Yes | Yes | Only historical | GitHub JSON files | N/A (static files) | Good for research only |
| **football-data.org** | Yes | No | No | No | Yes/Yes/Yes | Official REST | Yes (with key) | Team-level only |
| **Sportmonks** | Freemium | Yes | Yes | Yes | Yes/Yes/Yes | Official REST | Yes (with key) | Free tier very limited |
| **SofaScore** | Yes (unofficial) | Yes | Yes | Yes | Yes/Yes/Yes | Unofficial REST | No (needs proxy) | TOS risk |
| **OpenLigaDB** | Yes | No | No | No | Bundesliga-focused | Official REST | Yes (no key) | Wrong leagues |
| **FBref (via soccerdata)** | Yes | Yes | Yes | Yes | Yes/Yes/Yes | Scraping only | No | Python backend only |
| **FootyStats** | Freemium | Limited | No | Limited | Yes/Yes/Yes | Official REST | Yes (with key) | No xG data |

---

## DETAILED BREAKDOWN

### 1. FotMob Internal API -- BEST OPTION

- **URL:** `https://www.fotmob.com/api/data/leagues?id={leagueId}&ccode3=USA_NY`
- **What it provides:**
  - Player-level: xG, xGOT, xA, shots per 90, shots on target per 90, goals, assists, big chances created/missed, accurate passes, dribbles, FotMob rating
  - Team-level: full stats breakdown
  - Match-level: lineups, events, shot maps
- **Free:** Yes, no API key needed
- **API:** Unofficial REST endpoints (not documented, reverse-engineered from their web app)
- **League IDs:** EPL = 47, La Liga = 87, Champions League = 42
- **CORS:** No -- blocked by Cloudflare. Needs a proxy server
- **Data quality:** Opta-sourced, very high quality
- **Risk:** Endpoints can change without notice. No official support
- **How to use:** Python proxy server fetches from FotMob, serves to your browser
- **Verified endpoints:**
  - `GET /api/data/leagues?id=47` -- league overview + top player stats (xG, shots, assists, etc.)
  - `GET /api/matchDetails?matchId={id}` -- full match data with shot maps
  - `GET /api/playerData?id={playerId}` -- individual player career stats

### 2. Understat -- TOP PICK for xG

- **URL:** https://understat.com
- **Python packages:** `understat` (async), `understatapi` (sync)
- **What it provides:**
  - Per-shot xG values for every shot in every match
  - Player season totals: xG, xA, shots, key passes, goals, assists
  - Shot location (x, y coordinates on pitch)
  - Match-by-match breakdowns
- **Free:** Yes, completely free
- **API:** No official API. Data is embedded in HTML pages as encoded JSON. Python libraries parse it
- **Leagues:** EPL, La Liga, Bundesliga, Serie A, Ligue 1, RFPL -- **NO Champions League**
- **CORS:** N/A (scraping-based, needs Python backend)
- **Data quality:** Their own xG model, widely respected in analytics community
- **How to use:** `pip install understat` then use async Python to fetch player/match data
- **GitHub:** https://github.com/amosbastian/understat

### 3. API-Football (via API-Sports) -- BEST OFFICIAL API

- **URL:** https://www.api-football.com / https://api-sports.io
- **What it provides:**
  - Player stats per fixture: shots (total, on target), goals, assists, passes, tackles, duels, rating
  - Season aggregated player stats
  - Fixtures, standings, lineups, events
- **Free tier:** 100 requests/day, all endpoints accessible, limited to current season
- **API:** Official REST API, well-documented
- **Leagues:** 1,200+ competitions including EPL, La Liga, Champions League
- **CORS:** Yes, works from browser with API key in header
- **xG:** Not confirmed in free tier. Some advanced stats may be paid-only
- **How to use:** Register at api-sports.io, get free key, call endpoints
- **Docs:** https://api-sports.io/documentation/football/v3
- **Key endpoints:**
  - `GET /v3/players?id={id}&season=2025` -- player season stats
  - `GET /v3/fixtures/players?fixture={id}` -- per-match player stats
  - `GET /v3/players/topscorers?league=39&season=2025` -- top scorers

### 4. StatsBomb Open Data -- RESEARCH ONLY

- **URL:** https://github.com/statsbomb/open-data
- **Python package:** `statsbombpy`
- **What it provides:**
  - Event-level data: every pass, shot, dribble, tackle with x/y coordinates
  - xG per shot (StatsBomb's own model)
  - StatsBomb360 freeze-frame data (player positions at moment of event)
- **Free:** Yes, open data under license
- **API:** JSON files on GitHub + Python library to stream them
- **Leagues covered (FREE):**
  - EPL: Only 2003/04 and 2015/16
  - La Liga: 2004/05 through 2020/21
  - Champions League: Historical only (1999-2019)
  - **NO current season data**
- **CORS:** N/A (static GitHub files, can fetch from browser)
- **Verdict:** Amazing data quality but only historical. Not useful for current season predictions

### 5. football-data.org

- **URL:** https://www.football-data.org
- **What it provides (free tier):**
  - Fixtures, results, league tables
  - 12 competitions (including EPL, La Liga, UCL)
  - 10 calls/minute
- **Free:** Yes
- **API:** Official REST API with API key
- **Player stats:** NO -- free tier has no player-level data at all
- **xG/Shots:** NO
- **CORS:** Yes (with API key)
- **Verdict:** Useful for fixtures/standings only. No player stats on free tier

### 6. Sportmonks

- **URL:** https://www.sportmonks.com/football-api/
- **What it provides:**
  - xG, xA data (from 2024 season onward)
  - Player stats: shots, goals, assists, passes, tackles
  - 2,500+ leagues
- **Free tier:** Very limited (only a handful of leagues, low request quota)
- **API:** Official REST API, well-documented
- **CORS:** Yes (with API key)
- **Verdict:** Has the data but free tier is too restrictive for real use

### 7. SofaScore (Unofficial)

- **URL:** https://www.sofascore.com
- **Python package:** `sofascore-wrapper`
- **What it provides:**
  - Player stats, match stats, shot maps with xG
  - Opta-sourced data
- **Free:** Data is free but no official public API
- **API:** Unofficial, reverse-engineered endpoints
- **Leagues:** All major leagues
- **CORS:** No (needs proxy)
- **Risk:** Against TOS, endpoints change frequently, may block automated access
- **Verdict:** Rich data but legally risky and unreliable

### 8. FBref (via Python scraping libraries)

- **URL:** https://fbref.com
- **Python packages:** `soccerdata`, `ScraperFC`, `fbrefdata`
- **What it provides:**
  - Comprehensive player stats: xG, xA, shots, shots on target, key passes, progressive carries
  - Season aggregates and per-match logs
  - Data sourced from Opta/StatsBomb
- **Free:** Yes (the website is free)
- **API:** No API. Must scrape HTML pages
- **Leagues:** All major leagues including EPL, La Liga, Champions League
- **CORS:** N/A (scraping only, Python backend required)
- **Rate limits:** FBref rate-limits aggressively. ~3 seconds between requests recommended
- **Verdict:** Best free data for breadth and depth, but scraping-only and slow

### 9. OpenLigaDB

- **URL:** https://www.openligadb.de
- **What it provides:** Match fixtures, scores, standings
- **Free:** Yes, no API key required
- **Player stats:** No
- **Leagues:** Primarily Bundesliga and German football
- **CORS:** Yes
- **Verdict:** Wrong leagues, no player stats. Not useful for this project

### 10. FootyStats API

- **URL:** https://footystats.org/api
- **What it provides:** Team stats, league stats, some player data
- **Free tier:** Limited requests, basic stats only
- **xG:** No
- **Verdict:** Not suitable -- no xG, limited player data

---

## RECOMMENDED ARCHITECTURE

For your betting model dashboard, here is the recommended setup:

### Option A: Python Proxy + FotMob (Fastest to ship)

```
Browser (JS) --> Your Python Proxy Server --> FotMob API
                                          --> Understat (for xG depth)
```

- Python Flask/FastAPI server running locally or on a VPS
- Server fetches from FotMob (all 3 leagues) and Understat (EPL + La Liga xG)
- Server caches responses (15-30 min TTL)
- Browser calls your proxy with CORS headers enabled
- **Covers:** EPL, La Liga, Champions League
- **Data:** xG, xGOT, xA, shots, shots on target, assists, big chances, ratings

### Option B: API-Football Official (Most reliable, limited volume)

```
Browser (JS) --> API-Football (direct, CORS supported)
```

- 100 free requests/day
- Official, documented, reliable
- May not have xG in free tier
- Good for supplementing FotMob data with fixture/lineup info

### Option C: Hybrid (Best of both)

```
Browser (JS) --> Your Python Proxy --> FotMob (player stats, xG, shots)
                                   --> Understat (shot-level xG, locations)
            --> API-Football (direct) --> fixtures, lineups, live scores
```

This gives you the most complete picture with zero cost.

---

## KEY PYTHON PACKAGES TO INSTALL

```bash
pip install understat        # Async Understat xG data
pip install understatapi     # Sync Understat wrapper
pip install soccerdata       # FBref + Understat + more
pip install statsbombpy      # StatsBomb open data
pip install requests         # For FotMob API calls
pip install flask-cors       # For your proxy server
```

---

## SOURCES

- [FotMob](https://www.fotmob.com)
- [Understat](https://understat.com)
- [API-Football](https://www.api-football.com)
- [StatsBomb Open Data (GitHub)](https://github.com/statsbomb/open-data)
- [football-data.org](https://www.football-data.org)
- [Sportmonks Football API](https://www.sportmonks.com/football-api/)
- [SofaScore](https://www.sofascore.com)
- [FBref](https://fbref.com)
- [soccerdata Python package](https://github.com/probberechts/soccerdata)
- [understat Python package](https://github.com/amosbastian/understat)
- [understatAPI Python package](https://github.com/collinb9/understatAPI)
- [fotmob-api Python package](https://github.com/C-Roensholt/fotmob-api)
- [OpenLigaDB](https://publicapi.dev/open-liga-db-api)
- [FootyStats API](https://footystats.org/api)
- [Joe Kampschmidt's Guide to Football APIs](https://www.jokecamp.com/blog/guide-to-football-and-soccer-data-and-apis/)
- [McKay Johns - Where to Get Free Football Data](https://mckayjohns.substack.com/p/where-to-get-free-football-data)
