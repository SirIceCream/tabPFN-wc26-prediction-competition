# Data

This project uses public football match data as raw inputs for the TabPFN baseline and later feature engineering.

## Raw Sources

### `martj42/international_results`

- Local path: `data/raw/international_results/`
- Source: `https://github.com/martj42/international_results.git`
- License: CC0-1.0
- Current local commit: `85d5335f95a2a26be32c4c64a51c6f7e5b23ebd8`

Files cloned:

- `results.csv`: international match results and future fixtures
- `shootouts.csv`: penalty shootout winners
- `goalscorers.csv`: goal scorer events
- `former_names.csv`: historical team names

At setup time, `results.csv` has `49,477` data rows plus a header row. The file includes historical played matches and some future fixture rows where `home_score` and `away_score` are `NA`.

Important source assumptions:

- The dataset covers men's full internationals.
- Olympic matches, B-team matches, U-23 matches, and league select-team matches are excluded by the dataset maintainer.
- Home and away team names use current national team names.
- Country names use the country name at the time and place of the match.
- Full-time scores include extra time but do not include penalty shootout goals.

### Prior Labs starter baseline

- Local path: `tabpfn-football-predictions/`
- Source: `https://github.com/PriorLabs/tabpfn-football-predictions.git`
- Current local commit: `20c449358eb736d8a05a6d2d4dbda8c37cde5cff`

The starter baseline reads `results.csv` and can download the latest raw `results.csv` directly from `martj42/international_results` when run with `--refresh`.

## Directory Policy

- Keep exact upstream clones in `data/raw/`.
- Do not hand-edit files under `data/raw/international_results/`.
- Put derived files in a future `data/processed/` directory.
- Put model outputs in a future `outputs/` directory or keep them inside the working model directory if they are temporary.
- Document every non-obvious data transformation here before relying on it for submissions.

## Refreshing Data

To update the raw data clone:

```bash
cd data/raw/international_results
git pull
```

Then record the new commit:

```bash
git rev-parse HEAD
```

If using the starter baseline's downloader instead:

```bash
cd tabpfn-football-predictions
python predict.py --refresh
```

That refreshes the starter directory's local `results.csv`, not the raw data clone.

## Initial Modeling Notes

The first model should use only `results.csv` because the starter baseline already supports it. Later improvements can test:

- adding shootout-aware knockout labels from `shootouts.csv`
- recency weighting by tournament type and qualification cycle
- team-name normalization checks against the competition fixture list
- host-country and travel features for United States, Canada, and Mexico venues
- calibration checks for draw probabilities
