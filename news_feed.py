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

    now = datetime.now(timezone.utc)
    payload = {
        "updated": now.isoformat(),
        "updated_unix": int(now.timestamp()),
        "source": "espn",
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
