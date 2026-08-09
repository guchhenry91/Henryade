"""
Small quota-aware API-Football client for the news feed.

Mirrors the proven client in henrys-match-engine: same host, same header, same
per-run budget guard. The free plan allows ~100 requests/day, so every caller
must spend deliberately — see news_feed.py for the game-day gating that keeps us
well under the cap.

Key comes from the API_FOOTBALL env var (a GitHub Actions environment secret).
"""
import json
import os
import urllib.parse
import urllib.request

BASE = "https://v3.football.api-sports.io"

# API-Football league ids for the leagues the model covers.
LEAGUE_IDS = {
    "epl": 39, "laliga": 140, "bundesliga": 78,
    "seriea": 135, "ligue1": 61, "ucl": 2, "europa": 3,
}


class QuotaExhausted(RuntimeError):
    pass


class Client:
    def __init__(self, key=None, limit=40):
        self.key = key or os.environ.get("API_FOOTBALL")
        if not self.key:
            raise RuntimeError("API_FOOTBALL is not set")
        self.limit = limit          # hard per-run request budget
        self.used = 0

    def get(self, path, **params):
        if self.used >= self.limit:
            raise QuotaExhausted(f"per-run budget exhausted ({self.limit})")
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        url = f"{BASE}/{path.lstrip('/')}" + (f"?{query}" if query else "")
        req = urllib.request.Request(
            url, headers={"x-apisports-key": self.key,
                          "User-Agent": "henryade-newsfeed/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        self.used += 1
        errors = payload.get("errors")
        # API-Football returns errors as a dict (or sometimes list). Empty = OK.
        if errors:
            raise RuntimeError(f"API-Football error on {path}: {errors}")
        return payload.get("response") or []

    def status(self):
        """Account/quota info — safe to log (no fixtures data). Best-effort."""
        try:
            req = urllib.request.Request(
                f"{BASE}/status", headers={"x-apisports-key": self.key,
                                           "User-Agent": "henryade-newsfeed/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            self.used += 1
            resp_obj = payload.get("response") or {}
            reqs = (resp_obj.get("requests") or {})
            return {"current": reqs.get("current"), "limit_day": reqs.get("limit_day")}
        except Exception as e:
            return {"error": repr(e)}
