"""
Poisson Correct Score Model
Uses real odds from The Odds API + Poisson distribution
to calculate correct score probabilities and find value bets.
"""

import math
from itertools import product

# ── Poisson probability ────────────────────────────────────────────────────────
def poisson_prob(lam, k):
    """P(X=k) where X ~ Poisson(lambda)"""
    return (math.exp(-lam) * lam**k) / math.factorial(k)

# ── Correct score grid ─────────────────────────────────────────────────────────
def correct_score_probs(home_xg, away_xg, max_goals=5):
    """
    Returns dict of {(home_goals, away_goals): probability}
    using independent Poisson distributions for each team.
    """
    scores = {}
    for h, a in product(range(max_goals + 1), repeat=2):
        scores[(h, a)] = poisson_prob(home_xg, h) * poisson_prob(away_xg, a)
    return scores

# ── Implied probability from decimal odds ─────────────────────────────────────
def implied_prob(decimal_odds):
    return 1 / decimal_odds

# ── Value edge ────────────────────────────────────────────────────────────────
def value_edge(model_prob, decimal_odds):
    imp = implied_prob(decimal_odds)
    return round((model_prob - imp) * 100, 2)

# ── Top N scores ──────────────────────────────────────────────────────────────
def top_scores(scores, n=5):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[:n]

# ── xG estimates from qualifying stats ────────────────────────────────────────
# Format: (team, home_xg, away_xg, bookmaker_h2h_odds: [home, draw, away])
# xG estimated from goals scored/conceded per game in qualifying
# home_xg = avg goals scored at home / away_xg = avg goals scored away

MATCHES = [
    {
        "home": "Italy",
        "away": "Northern Ireland",
        "home_xg": 2.1,   # 21 goals / 8 games, strong home side
        "away_xg": 0.5,   # NI 7 goals / 6 games, historically can't score vs Italy
        "odds_home": 1.25,
        "odds_draw": 5.50,
        "odds_away": 13.0,
        "totals_over": 1.75,
        "totals_under": 2.00,
    },
    {
        "home": "Wales",
        "away": "Bosnia & Herzegovina",
        "home_xg": 1.8,   # Wales strong attack, 7-1 last game but key injuries
        "away_xg": 1.0,   # Bosnia solid, Dzeko threat, 5 goals in qualifying
        "odds_home": 1.70,
        "odds_draw": 3.60,
        "odds_away": 5.20,
        "totals_over": 1.91,
        "totals_under": 1.80,
    },
    {
        "home": "Ukraine",
        "away": "Sweden",
        "home_xg": 1.7,   # Ukraine solid but missing Zinchenko
        "away_xg": 0.6,   # Sweden 0 wins, 4 goals in 6 games, missing Isak/Kulusevski
        "odds_home": 3.35,
        "odds_draw": 3.20,
        "odds_away": 2.30,
        "totals_over": 2.15,
        "totals_under": 1.62,
    },
    {
        "home": "Poland",
        "away": "Albania",
        "home_xg": 1.9,   # 14 goals in 8 games, Lewandowski
        "away_xg": 0.7,   # Albania 1-0 away wins, tight defensive unit
        "odds_home": 1.67,
        "odds_draw": 3.50,
        "odds_away": 5.80,
        "totals_over": 2.20,
        "totals_under": 1.62,
    },
    {
        "home": "Turkey",
        "away": "Romania",
        "home_xg": 1.6,   # Turkey drew 2-2 Spain, Güler threat, missing Celik/Demiral
        "away_xg": 1.1,   # Romania capable away side, Man dangerous
        "odds_home": 1.40,
        "odds_draw": 4.90,
        "odds_away": 7.20,
        "totals_over": 1.55,
        "totals_under": 2.30,
    },
    {
        "home": "Slovakia",
        "away": "Kosovo",
        "home_xg": 1.2,   # Slovakia solid at home, 0 goals conceded last 5 home
        "away_xg": 0.8,   # Kosovo 5 unbeaten, 4 clean sheets, but low scorers
        "odds_home": 2.30,
        "odds_draw": 3.10,
        "odds_away": 3.50,
        "totals_over": 2.40,
        "totals_under": 1.53,
    },
    {
        "home": "Denmark",
        "away": "North Macedonia",
        "home_xg": 2.3,   # Denmark heavy favourites, Hojlund in form
        "away_xg": 0.4,   # N. Macedonia lost 7-1 to Wales, confidence shot
        "odds_home": 1.23,
        "odds_draw": 6.10,
        "odds_away": 15.0,
        "totals_over": 1.62,
        "totals_under": 2.15,
    },
    {
        "home": "Czech Republic",
        "away": "Ireland",
        "home_xg": 1.8,   # Unbeaten 17 home qualifiers, Schick available
        "away_xg": 0.9,   # Parrott in form but 2 key suspensions
        "odds_home": 1.90,
        "odds_draw": 3.45,
        "odds_away": 4.20,
        "totals_over": 2.10,
        "totals_under": 1.67,
    },
]

# ── Run model ──────────────────────────────────────────────────────────────────
def run_model():
    results = []

    for match in MATCHES:
        home = match["home"]
        away = match["away"]
        scores = correct_score_probs(match["home_xg"], match["away_xg"])

        # Win/draw/loss probabilities from model
        home_win_prob = sum(p for (h, a), p in scores.items() if h > a)
        draw_prob = sum(p for (h, a), p in scores.items() if h == a)
        away_win_prob = sum(p for (h, a), p in scores.items() if a > h)

        # Expected total goals
        exp_total = match["home_xg"] + match["away_xg"]
        over_prob = sum(p for (h, a), p in scores.items() if h + a > 2)
        under_prob = sum(p for (h, a), p in scores.items() if h + a <= 2)
        btts_prob = sum(p for (h, a), p in scores.items() if h > 0 and a > 0)

        # Value edges
        home_edge = value_edge(home_win_prob, match["odds_home"])
        draw_edge = value_edge(draw_prob, match["odds_draw"])
        away_edge = value_edge(away_win_prob, match["odds_away"])
        over_edge = value_edge(over_prob, match["totals_over"])
        under_edge = value_edge(under_prob, match["totals_under"])

        best_scores = top_scores(scores, n=5)

        results.append({
            "match": f"{home} vs {away}",
            "home_win": round(home_win_prob * 100, 1),
            "draw": round(draw_prob * 100, 1),
            "away_win": round(away_win_prob * 100, 1),
            "home_edge": home_edge,
            "draw_edge": draw_edge,
            "away_edge": away_edge,
            "over_prob": round(over_prob * 100, 1),
            "under_prob": round(under_prob * 100, 1),
            "over_edge": over_edge,
            "under_edge": under_edge,
            "btts_prob": round(btts_prob * 100, 1),
            "top_scores": best_scores,
            "exp_goals": round(exp_total, 2),
        })

    return results

def print_report(results):
    print("=" * 65)
    print("  POISSON CORRECT SCORE MODEL — WCQ March 26, 2026")
    print("=" * 65)

    for r in results:
        print(f"\n{'─'*65}")
        print(f"  {r['match']}")
        print(f"{'─'*65}")
        print(f"  Model Probs:  Home {r['home_win']}%  |  Draw {r['draw']}%  |  Away {r['away_win']}%")
        print(f"  Value Edges:  Home {r['home_edge']:+}%  |  Draw {r['draw_edge']:+}%  |  Away {r['away_edge']:+}%")
        print(f"  Over 2.5: {r['over_prob']}% (edge {r['over_edge']:+}%)  |  Under 2.5: {r['under_prob']}% (edge {r['under_edge']:+}%)")
        print(f"  BTTS: {r['btts_prob']}%  |  Expected Goals: {r['exp_goals']}")
        print(f"  Top Correct Scores:")
        for i, ((h, a), p) in enumerate(r['top_scores'], 1):
            print(f"    {i}. {h}-{a}  →  {round(p*100, 2)}%")

    print(f"\n{'='*65}")
    print("  VALUE BETS SUMMARY (edge > +3%)")
    print(f"{'='*65}")
    for r in results:
        edges = [
            (f"{r['match']} — Home Win", r['home_edge']),
            (f"{r['match']} — Draw", r['draw_edge']),
            (f"{r['match']} — Away Win", r['away_edge']),
            (f"{r['match']} — Over 2.5", r['over_edge']),
            (f"{r['match']} — Under 2.5", r['under_edge']),
        ]
        for label, edge in edges:
            if edge > 3:
                print(f"  ✓ {label}  →  +{edge}% edge")

if __name__ == "__main__":
    results = run_model()
    print_report(results)
