# TabPFN World Cup 2026 Prediction Competition Rules

This file records the working rules for our local project. Treat these as the source of truth for development decisions until the official competition page or organizer instructions say otherwise.

## Objective

Build a model that predicts World Cup 2026 football match outcomes using TabPFN and engineered football features.

The target is a three-class match result:

- `home_win`
- `draw`
- `away_win`

## Baseline

Use `tabpfn-football-predictions/` as the starter implementation.

The baseline:

- trains a `TabPFNClassifier`
- engineers chronological features without using future match outcomes
- uses ELO ratings, recent form, head-to-head results, rest days, venue neutrality, and tournament importance
- outputs one probability for each result class

## Submission Shape

Predictions should preserve the starter repository's output columns unless the official schema requires a change:

- `date`
- `home_team`
- `away_team`
- `predicted`
- `p_home_win`
- `p_draw`
- `p_away_win`

Probability columns must be numeric, non-negative, and should sum to `1.0` per match after any post-processing.

## Modeling Rules

- Do not train on future results relative to the match being predicted.
- Chronological features must use only matches played before kickoff.
- Raw historical data should remain unchanged in `data/raw/`.
- Add cleaned, derived, or model-ready datasets outside `data/raw/`.
- Any manual team-name mappings, fixture edits, or excluded matches must be documented in `docs/data.md`.
- Keep model outputs reproducible by recording source dataset revisions and major modeling assumptions.

## Validation

Use held-out chronological validation, not random splits.

Recommended first validation pass:

- train on historical matches before the validation month
- validate on the most recent completed calendar month with enough played matches
- report accuracy and multiclass log-loss

Prefer log-loss when comparing models because the competition cares about calibrated probabilities, not just the top predicted class.

## Open Items

- Confirm the official competition deadline.
- Confirm whether knockout matches are scored as regulation/extra-time results or include penalty shootout winners.
- Confirm whether the final submission requires fixture IDs in addition to team/date columns.
- Confirm whether external data beyond public football results is allowed.
- Confirm the official scoring metric and tie-break rules.
