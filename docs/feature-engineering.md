# Feature Engineering Ideas

This file tracks candidate features and how we should add them without breaking chronological validity.

## Betting Odds / Market Prior

Betting odds can be useful because they aggregate public information, injuries, team news, expert opinions, and market sentiment. They should be treated as a market prior, not as a normal historical team statistic.

Before using this in an official submission, confirm that the competition allows external market data.

### Data to Collect

For each fixture, collect 1X2 odds from several providers:

- home win odds
- draw odds
- away win odds
- provider name
- timestamp when collected
- source URL or export file

Store raw collected odds in a separate file, for example:

```text
data/processed/round_of_32_betting_odds.csv
```

Suggested schema:

```csv
match_no,date,home_team,away_team,provider,collected_at,home_odds,draw_odds,away_odds
```

### Convert Odds to Probabilities

Decimal odds imply raw probabilities:

```text
raw_home = 1 / home_odds
raw_draw = 1 / draw_odds
raw_away = 1 / away_odds
```

Bookmakers include margin, so normalize:

```text
market_home = raw_home / (raw_home + raw_draw + raw_away)
market_draw = raw_draw / (raw_home + raw_draw + raw_away)
market_away = raw_away / (raw_home + raw_draw + raw_away)
```

When multiple providers are available, aggregate with median probabilities to reduce one-provider noise:

```text
market_home_median
market_draw_median
market_away_median
market_provider_count
market_home_spread
market_draw_spread
market_away_spread
```

The spread is the difference between highest and lowest provider-implied probability. A wide spread means the market is uncertain or providers disagree.

### Option A: Add Odds as TabPFN Features

Add these columns to the model feature matrix:

```text
market_home
market_draw
market_away
market_provider_count
market_home_spread
market_draw_spread
market_away_spread
model_vs_market_home
model_vs_market_draw
model_vs_market_away
```

The `model_vs_market_*` features compare our baseline probability to the market probability.

Risk: we usually do not have historical odds for the old training matches, so these features may only exist for future fixtures. TabPFN needs a consistent feature matrix for both training and prediction. Without historical odds, this option is weaker unless we source historical odds too.

### Option B: Blend Market and Model Outputs

This is the cleaner first implementation.

Run the current TabPFN baseline first:

```text
model_home
model_draw
model_away
```

Then blend with the market:

```text
final_home = weight_model * model_home + weight_market * market_home
final_draw = weight_model * model_draw + weight_market * market_draw
final_away = weight_model * model_away + weight_market * market_away
```

Example starting weights:

```text
weight_model = 0.65
weight_market = 0.35
```

Normalize the final probabilities after blending.

This avoids retraining TabPFN on sparse odds data and gives us an adjustable post-processing layer.

### Evaluation

Compare at least these variants:

- baseline TabPFN only
- market only
- 80/20 model-market blend
- 65/35 model-market blend
- 50/50 model-market blend

Use chronological validation where possible. If historical odds are not available, treat this as a submission-time calibration layer and document the timestamp of odds collection.

### Leakage Rules

- Odds must be collected before the match lock time.
- Do not update submitted probabilities after lineups, injuries, or market moves if the competition lock has already passed.
- Keep `collected_at` timestamps for reproducibility.
- Do not use live odds after kickoff.

## Current Recommendation

Implement betting odds first as a post-model blending layer, not as TabPFN training features. That gives us a distinct output while keeping the current baseline stable.

## Implemented Adjustment Layer

The repo now has a deterministic post-model adjustment script:

```text
scripts/adjust_probabilities.py
```

Inputs:

```text
outputs/round_of_32_submission.csv
data/processed/round_of_32_fixtures.csv
data/processed/round_of_32_team_context.csv
data/processed/round_of_32_market_odds.csv
```

The team-context file supports:

- `confederation`
- `is_host`
- `group_points`
- `group_goal_diff`
- `prior_run_score`

The market-odds file supports multiple providers per match and converts decimal odds to normalized implied probabilities before blending.

Example run:

```bash
tabpfn-football-predictions/.venv/bin/python scripts/adjust_probabilities.py \
  outputs/round_of_32_submission.csv \
  data/processed/round_of_32_fixtures.csv \
  data/processed/round_of_32_team_context.csv \
  outputs/round_of_32_adjusted_submission.csv \
  --market-odds-csv data/processed/round_of_32_market_odds.csv
```

The adjustment layer currently applies:

- group-points edge
- group-goal-difference edge
- prior tournament run edge
- explicit host edge for United States, Mexico, and Canada when playing in their own country
- small cross-confederation uncertainty shrink toward `1/3, 1/3, 1/3`
- optional market blend

The uncertainty factor is deliberately symmetric. It does not randomly push toward either team; it slightly reduces overconfidence in cross-confederation matchups.

## Current Populated Sources

Group-stage points and goal-difference inputs are populated from the current CBS Sports group standings/results page.

Market odds are populated from the FOX Sports Round of 32 odds page, which cites FanDuel Sportsbook moneylines as of June 27. American odds were converted to decimal odds before saving in:

```text
data/processed/round_of_32_market_odds.csv
```

`prior_run_score` is still a hand-built heuristic. It summarizes recent senior men's international tournament strength on a simple scale, using World Cup plus major confederation tournament performance. Treat this as a first-pass feature, not a fully audited ranking.
