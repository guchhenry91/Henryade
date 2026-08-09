#!/usr/bin/env python3
"""
news_feed.py — auto-collects team news, transfers, injuries, and (on game days)
confirmed lineups for the leagues the betting model covers, and writes news.json.

Runs unattended from GitHub Actions every ~30 min. All data is free from ESPN's
public API (no key). The frontend reads news.json to show a news/injury panel and
to drop goal-scorer picks for players who are injured or not in the confirmed XI.

Exit code is always 0 on partial failure — a single dead league must not break the
whole feed. Writes news.json only from whatever it successfully collected.
"""
import json
import os
import sys
import time
from datetime import datetime, timezone

import requests

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "henryade-newsfeed/1.0"})
TIMEOUT = 12

# Soccer leagues — get news, injuries, AND confirmed lineups on game day.
SOCCER_LEAGUES = {
    "epl":        {"name": "Premier League",  "espn": "soccer/eng.1"},
    "laliga":     {"name": "La Liga",         "espn": "soccer/esp.1"},
    "bundesliga": {"name": "Bundesliga",      "espn": "soccer/ger.1"},
    "seriea":     {"name": "Serie A",         "espn": "soccer/ita.1"},
    "ligue1":     {"name": "Ligue 1",         "espn": "soccer/fra.1"},
    "ucl":        {"name": "Champions League","espn": "soccer/uefa.champions"},
    "europa":     {"name": "Europa League",   "espn": "soccer/uefa.europa"},
}

# US sports — news + injuries only (no soccer-style starting XI feed).
OTHER_LEAGUES = {
    "nfl": {"name": "NFL", "espn": "football/nfl"},
    "nba": {"name": "NBA", "espn": "basketball/nba"},
    "nhl": {"name": "NHL", "espn": "hockey/nhl"},
    "mlb": {"name": "MLB", "espn": "baseball/mlb"},
}

# Only pull lineups for games kicking off within this window (or already live).
LINEUP_WINDOW_HOURS = 8
# Cap summary calls per league per run so a busy matchday can't blow the runtime.
MAX_LINEUP_EVENTS = 12

ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports"

# ── API-Football (optional, higher-quality soccer injuries + confirmed XIs) ─────
# Enabled only when the API_FOOTBALL env var (a GitHub Actions secret) is present.
# Free plan ~100 req/day, so spend is tied strictly to real fixtures near kickoff.
try:
    from api_football import Client as AFClient, QuotaExhausted, LEAGUE_IDS as AF_LEAGUE_IDS
    _AF_AVAILABLE = True
except Exception:
    _AF_AVAILABLE = False

STATE_PATH = "news_state.json"
AF_FIXTURES_TTL = 6 * 3600      # refresh a league's fixture list at most every 6h
AF_LINEUP_WINDOW_MIN = 55       # fetch confirmed XI only within this many min of KO
AF_RUN_BUDGET = 30              # hard per-run request cap (free plan is ~100/day)


def _af_season():
    """API-Football season = the year the season starts (Aug onward = new season)."""
    now = datetime.now(timezone.utc)
    return now.year if now.month >= 8 else now.year - 1


def load_state():
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, ValueError):
        return {}


def _prune_state(state, now_ts):
    """Drop fixture-level markers older than 2 days so the state file stays small."""
    cutoff = now_ts - 2 * 86400
    for key in ("af_lineup_attempted", "af_inj_fixture"):
        d = state.get(key) or {}
        state[key] = {k: v for k, v in d.items()
                      if isinstance(v, (int, float)) and v > cutoff
                      or isinstance(v, str)}  # date-string markers pruned by date below
    # date-string injury markers: keep only today's
    today = datetime.now(timezone.utc).date().isoformat()
    inj = state.get("af_inj_fixture") or {}
    state["af_inj_fixture"] = {k: v for k, v in inj.items() if v == today}


def af_fixtures_for_league(client, state, lkey, season, now):
    """Today's fixtures for a league, cached in state for AF_FIXTURES_TTL."""
    cache = (state.setdefault("af_fixtures", {})).get(lkey)
    today = now.date().isoformat()
    if cache and cache.get("date") == today and (now.timestamp() - cache.get("ts", 0)) < AF_FIXTURES_TTL:
        return cache["items"], False
    rows = client.get("fixtures", league=AF_LEAGUE_IDS[lkey], season=season,
                      date=today, timezone="UTC")
    items = []
    for r in rows:
        fx, teams = r.get("fixture", {}), r.get("teams", {})
        items.append({
            "id": fx.get("id"),
            "home": (teams.get("home") or {}).get("name", ""),
            "away": (teams.get("away") or {}).get("name", ""),
            "ko": fx.get("date", ""),
            "status": (fx.get("status") or {}).get("short", ""),
        })
    state["af_fixtures"][lkey] = {"date": today, "ts": now.timestamp(), "items": items}
    return items, True


def af_enrich_league(client, state, lkey, league_obj, season, now):
    """
    Populate a soccer league's injuries + confirmed lineups from API-Football,
    spending quota only on today's fixtures (injuries once/day, XI near kickoff).
    Mutates league_obj in place. Returns True if anything changed.
    """
    changed = False
    try:
        fixtures, _ = af_fixtures_for_league(client, state, lkey, season, now)
    except QuotaExhausted:
        return changed
    if not fixtures:
        return changed

    # Publish today's fixtures so the News tab has real content from the working
    # API (independent of ESPN, which blocks GitHub's servers).
    fx_public = [{"home": fx["home"], "away": fx["away"], "ko": fx["ko"],
                  "status": fx.get("status", "")} for fx in fixtures if fx.get("home")]
    if fx_public and league_obj.get("fixtures") != fx_public:
        league_obj["fixtures"] = fx_public
        changed = True

    injuries = league_obj.setdefault("injuries", {})
    lineups = league_obj.setdefault("lineups", {})
    inj_seen = state.setdefault("af_inj_fixture", {})
    xi_done = state.setdefault("af_lineup_attempted", {})
    today = now.date().isoformat()

    for fx in fixtures:
        fid = fx.get("id")
        if not fid:
            continue
        try:
            ko = datetime.fromisoformat(fx["ko"].replace("Z", "+00:00"))
        except Exception:
            continue
        mins_to_ko = (ko - now).total_seconds() / 60

        # Injuries: once per fixture per day, for games in the next ~48h.
        if str(fid) not in inj_seen and -3 < mins_to_ko / 60 < 48:
            try:
                rows = client.get("injuries", fixture=fid)
                for r in rows:
                    team = (r.get("team") or {}).get("name", "")
                    player = (r.get("player") or {}).get("name", "")
                    reason = (r.get("player") or {}).get("reason") or r.get("reason") or ""
                    if team and player:
                        injuries.setdefault(team, [])
                        if not any(p["player"] == player for p in injuries[team]):
                            injuries[team].append({"player": player, "status": reason or "Out",
                                                   "detail": reason})
                            changed = True
                inj_seen[str(fid)] = today
                changed = True
            except QuotaExhausted:
                return changed
            except Exception:
                inj_seen[str(fid)] = today  # don't retry a failing endpoint all day

        # Confirmed XI: only within the kickoff window, one attempt per fixture.
        if 0 < mins_to_ko <= AF_LINEUP_WINDOW_MIN and str(fid) not in xi_done:
            try:
                rows = client.get("fixtures/lineups", fixture=fid)
            except QuotaExhausted:
                return changed
            except Exception:
                rows = []
            xi_done[str(fid)] = now.timestamp()
            changed = True
            if len(rows) == 2:
                sides = []
                for row in rows:
                    team = (row.get("team") or {}).get("name", "")
                    xi = [(i.get("player") or {}).get("name", "") for i in row.get("startXI", [])]
                    xi = [n for n in xi if n]
                    sides.append({"team": team, "formation": row.get("formation"), "xi": xi})
                if any(len(s["xi"]) >= 11 for s in sides):
                    lineups[str(fid)] = {
                        "name": f"{fx['home']} vs {fx['away']}",
                        "kickoff": fx["ko"], "state": "pre", "confirmed": True,
                        "sides": sides, "source": "API-Football",
                    }
    return changed


def af_enrich_soccer(leagues, state):
    """Run API-Football enrichment across all soccer leagues. Returns (used, changed)."""
    if not (_AF_AVAILABLE and os.environ.get("API_FOOTBALL")):
        return 0, False
    now = datetime.now(timezone.utc)
    season = _af_season()
    try:
        client = AFClient(limit=AF_RUN_BUDGET)
    except Exception as e:
        print(f"  api-football: disabled ({e})")
        return 0, False
    st = client.status()
    print(f"  api-football: quota {st.get('current')}/{st.get('limit_day')} season={season}")
    changed = False
    for lkey in SOCCER_LEAGUES:
        if lkey not in AF_LEAGUE_IDS or lkey not in leagues:
            continue
        try:
            if af_enrich_league(client, state, lkey, leagues[lkey], season, now):
                changed = True
        except QuotaExhausted:
            print("  api-football: per-run budget hit — stopping")
            break
        except Exception as e:
            print(f"  api-football {lkey}: {e}")
    _prune_state(state, now.timestamp())
    print(f"  api-football: {client.used} requests used this run")
    return client.used, changed


def _get(url):
    try:
        r = SESSION.get(url, timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def fetch_news(espn_path):
    """Headlines: transfers, team news, previews. Returns list of dicts."""
    data = _get(f"{ESPN_BASE}/{espn_path}/news")
    if not data:
        return []
    out = []
    for a in data.get("articles", [])[:12]:
        links = a.get("links", {}) or {}
        web = (links.get("web", {}) or {}).get("href", "")
        out.append({
            "title": a.get("headline", ""),
            "desc": (a.get("description", "") or "")[:240],
            "published": a.get("published", ""),
            "type": a.get("type", ""),
            "link": web,
        })
    return out


def fetch_injuries(espn_path):
    """League-wide injuries grouped by team -> [{player, status, detail}]."""
    data = _get(f"{ESPN_BASE}/{espn_path}/injuries")
    if not data:
        return {}
    out = {}
    for grp in data.get("injuries", []):
        team = grp.get("displayName") or grp.get("team", {}).get("displayName", "")
        items = []
        for inj in grp.get("injuries", []):
            ath = inj.get("athlete", {}) or {}
            detail = inj.get("details", {}) or {}
            items.append({
                "player": ath.get("displayName", ""),
                "status": inj.get("status", ""),
                "detail": inj.get("shortComment") or detail.get("type", "") or "",
            })
        if team and items:
            out[team] = items
    return out


def fetch_lineups(espn_path):
    """
    Confirmed / probable starting XIs for imminent or live games.
    Only queries the summary endpoint for events inside the lineup window.
    """
    sb = _get(f"{ESPN_BASE}/{espn_path}/scoreboard")
    if not sb:
        return {}
    now = time.time()
    horizon = now + LINEUP_WINDOW_HOURS * 3600
    lineups = {}
    events = sb.get("events", [])[:30]
    queried = 0
    for ev in events:
        if queried >= MAX_LINEUP_EVENTS:
            break
        eid = ev.get("id")
        state = ev.get("status", {}).get("type", {}).get("state", "")  # pre | in | post
        if state == "post":
            continue
        # Parse kickoff time
        try:
            ko = datetime.fromisoformat(ev.get("date", "").replace("Z", "+00:00")).timestamp()
        except Exception:
            ko = now
        # Live games (state == "in") always; pre-games only within the window
        if state == "pre" and ko > horizon:
            continue

        summary = _get(f"{ESPN_BASE}/{espn_path}/summary?event={eid}")
        queried += 1
        if not summary:
            continue
        rosters = summary.get("rosters") or []
        sides = []
        for r in rosters:
            players = r.get("roster", []) or []
            starters = [
                (p.get("athlete", {}) or {}).get("displayName", "")
                for p in players if p.get("starter")
            ]
            starters = [s for s in starters if s]
            sides.append({
                "team": (r.get("team", {}) or {}).get("displayName", ""),
                "formation": r.get("formation"),
                "xi": starters,
            })
        # Only record if at least one side has a real XI (data present near kickoff)
        if any(s["xi"] for s in sides):
            comp = (ev.get("competitions") or [{}])[0]
            lineups[eid] = {
                "name": ev.get("name", ""),
                "kickoff": ev.get("date", ""),
                "state": state,
                "confirmed": state == "in" or all(len(s["xi"]) >= 11 for s in sides if s["xi"]),
                "sides": sides,
            }
    return lineups


def collect_league(key, cfg, with_lineups):
    league = {"name": cfg["name"], "headlines": [], "injuries": {}}
    league["headlines"] = fetch_news(cfg["espn"])
    league["injuries"] = fetch_injuries(cfg["espn"])
    if with_lineups:
        league["lineups"] = fetch_lineups(cfg["espn"])
    counts = (len(league["headlines"]), len(league["injuries"]),
              len(league.get("lineups", {})))
    print(f"  {key:11} news={counts[0]:2} injuries(teams)={counts[1]:2} lineups={counts[2]}")
    return league


def main():
    print(f"news_feed: collecting @ {datetime.now(timezone.utc).isoformat()}")
    leagues = {}

    for key, cfg in SOCCER_LEAGUES.items():
        try:
            leagues[key] = collect_league(key, cfg, with_lineups=True)
        except Exception as e:
            print(f"  {key}: FAILED {e!r}")

    for key, cfg in OTHER_LEAGUES.items():
        try:
            leagues[key] = collect_league(key, cfg, with_lineups=False)
        except Exception as e:
            print(f"  {key}: FAILED {e!r}")

    if not leagues:
        print("news_feed: collected nothing — leaving existing news.json untouched")
        return 0

    # Upgrade soccer injuries + confirmed lineups with API-Football (if key present).
    # This overrides ESPN's soccer data, which is sparse/empty for injuries.
    state = load_state()
    try:
        _, state_changed = af_enrich_soccer(leagues, state)
    except Exception as e:
        print(f"  api-football: enrichment failed ({e!r})")
        state_changed = False
    if state_changed:
        try:
            with open(STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=1)
        except Exception:
            pass

    now = datetime.now(timezone.utc)
    payload = {
        "updated": now.isoformat(),
        "updated_unix": int(now.timestamp()),
        "source": "espn+api-football",
        "leagues": leagues,
    }

    # Only rewrite when the actual CONTENT changed (ignore the timestamp), so the
    # GitHub Action commits + redeploys Render only when there's real news — not
    # every 30 min just because the clock moved.
    try:
        with open("news.json", encoding="utf-8") as f:
            existing = json.load(f)
        if existing.get("leagues") == leagues:
            print("news_feed: content unchanged — keeping existing news.json")
            return 0
    except (FileNotFoundError, ValueError):
        pass

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print(f"news_feed: wrote news.json ({len(leagues)} leagues)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
