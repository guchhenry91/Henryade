# Betting Model Audit: Best Practices vs Our Model
**Date:** 2026-04-08

## 1. Minimum Edge % (3% threshold)
- **Industry consensus:** Sharp bettors operate on 2-5% edges. Our 3% minimum is right in the sweet spot.
- **Action:** Keep 3%. Could experiment with 2% on MLB (our strongest sport) to increase volume.

## 2. Negative Binomial for Player Props
- **Verdict: Correct choice.** NB handles over-dispersion (player inconsistency) better than Poisson. It learns a consistency parameter per player, catching blow-up games Poisson misses.
- **Enhancement:** Consider Monte Carlo simulation as a secondary check. OpticOdds research shows combining parametric (NB) with simulation catches edge cases.

## 3. UNDER Bias (69% UNDER WR vs 46% OVER)
- **This is a known sharp pattern.** Public loves OVERs, books add extra juice to OVERs, creating systematic mispricing on UNDERs.
- **Action:** LEAN INTO IT. The UNDER edge is real and structural. BUT also investigate why OVERs are weak:
  - Check if the model underweights pace/game environment for OVERs
  - Check if injury-cascade OVER opportunities (teammate usage boosts) are being missed
  - Consider separate OVER and UNDER confidence thresholds

## 4. Quarter-Kelly with 3% Cap
- **Verdict: Appropriate for our situation.** At 60% WR on -110, full Kelly = ~20% stakes (way too aggressive). Quarter-Kelly = ~5%, capped at 3% = conservative and safe.
- **However:** At 64% WR on MLB, we might be leaving money on the table. Consider half-Kelly (capped at 4%) for MLB only where our edge is proven over larger sample.
- **The 10% daily exposure cap is solid** -- standard risk management.

## 5. CLV Targets
- **+1-2% average CLV** = consistently profitable bettor
- **+3-5% average CLV** = elite/sharp territory
- **Action:** Track CLV by sport. If MLB CLV is +3% but NBA CLV is flat, that confirms where to allocate bankroll.

## 6. Free Data Sources We're Missing
- **BallDontLie API** (free tier) -- real-time NBA scores, player stats, decades of historical data
- **Sports Game Odds API** -- specifically built for player props with PRA combos
- **NBA.com Usage Rate page** -- lineup-filtered usage data (critical for props)
- **Fantasy Team Advice** -- pace/environment data per game
- **Sports Injury Central (sicscore.com)** -- injury impact ratings

## 7. NBA Props: Why We're Weak & How to Fix It
The #1 factor sharp NBA models use that we likely don't:

- **Projected minutes modeling:** Minutes determine everything. If a player's minutes drop from 34 to 28, all props shift. We need a minutes projection layer.
- **Usage rate shifts from injuries/absences:** When a star sits, usage redistributes. Books are slow to reprice teammate props (30-90 min window). We need real-time injury cascade modeling.
- **Pace/game environment:** A fast-paced game (LAL vs ATL) vs slow (MIA vs NYK) changes total stat output by 10-15%.
- **Back-to-back detection:** Rest patterns affect NBA more than any other sport. Starters lose 2-4 minutes on B2Bs.
- **High-variance stat targeting:** Blocks, steals, 3PM are harder for books to price. Focus edge-hunting there.

## Priority Actions (Ranked)
1. **Add minutes projection model for NBA** -- biggest single improvement available
2. **Add injury cascade / usage redistribution logic** -- exploit the 30-90 min repricing window
3. **Add pace/game environment signal** -- easy to implement, improves both NBA and MLB
4. **Split OVER/UNDER confidence thresholds** -- lean into UNDER strength, raise OVER bar
5. **Track CLV by sport** -- confirm where edge is real vs lucky
6. **Consider half-Kelly for MLB** -- our strongest sport deserves more allocation

## Sources
- [OpticOdds: Probability Paths in Player Prop Modeling](https://opticodds.com/blog/probability-paths-in-player-prop-modeling)
- [OddsShopper: Why You Need to Be Betting Unders in 2024](https://www.oddsshopper.com/articles/betting-101/why-you-need-to-be-betting-unders-in-2024-how-to-make-money-sports-betting-y10)
- [betstamp: Kelly Criterion Education](https://betstamp.com/education/kelly-criterion)
- [OddsJam: CLV Education](https://oddsjam.com/betting-education/closing-line-value)
- [Unabated: NBA Prop Betting Strategy](https://unabated.com/articles/fine-tune-your-nba-prop-betting-strategy-using-unabated-nba)
- [Leans.ai: NBA Player Prop Strategy 2026](https://leans.ai/nba-player-prop-strategy/)
- [Fantasy Team Advice: NBA Usage Rate by Lineup](https://fantasyteamadvice.com/nba/usage-rate)
- [Covers: NBA Prop Betting Tips](https://www.covers.com/nba/prop-betting-tips)
- [Binomial Basketball: Predicting Sensational Stats](https://www.binomialbasketball.com/p/predicting-sensational-stats-pt-3)
- [SportBot AI: Sports Betting Profitability Statistics 2026](https://www.sportbotai.com/stats/sports-betting-profitability)
