# Baseline Run

This records the first successful baseline run from the Prior Labs starter repository.

## Environment

Working directory:

```bash
cd tabpfn-football-predictions
```

Python environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

The baseline uses `tabpfn-client`, which opens a browser login flow on first use.

## Command

```bash
.venv/bin/python predict.py
```

## Result

Run date: `2026-06-26`

The baseline loaded `results.csv`, built chronological features, trained TabPFN through the client API, and generated:

```text
tabpfn-football-predictions/predictions_20260626.csv
```

The sample output was copied into the parent project at:

```text
outputs/baseline_predictions_20260626.csv
```

Backtest:

```text
Backtest 2026-05 (26 matches): accuracy 85%, log-loss 0.531
```

The run emitted this warning during backtest:

```text
The y_prob values do not sum to one. Make sure to pass probabilities.
```

We should check probability normalization before treating log-loss comparisons as reliable.

## Output Schema

```text
date,home_team,away_team,predicted,p_home_win,p_draw,p_away_win
```

Example rows:

```csv
date,home_team,away_team,predicted,p_home_win,p_draw,p_away_win
2026-06-27,DR Congo,Uzbekistan,away_win,0.29055118560791016,0.2967667579650879,0.41268211603164673
2026-06-27,Colombia,Portugal,home_win,0.34732794761657715,0.3090473413467407,0.3436247706413269
2026-06-27,Panama,England,away_win,0.07344923913478851,0.1581539511680603,0.7683968544006348
```

## Immediate Follow-Ups

- Normalize output probabilities before computing log-loss or submitting.
- Move generated prediction artifacts out of the starter submodule before tracking them in the parent project.
- Add a wrapper script in the parent project so future runs can write to `outputs/` instead of dirtying the upstream starter checkout.
