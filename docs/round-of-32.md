# Round of 32 Submission

This file records the official upload requirements for the Round of 32.

## Status

- Round: `Round of 32`
- State: `Open`
- Deadline shown in UI: `Closes in 1 day`
- Submission type: upload a CSV of match-outcome probabilities for this round

## Required CSV Format

The upload file must have exactly this header row:

```csv
date,home_team,away_team,p_home_win,p_draw,p_away_win
```

Rules:

- Include one row per match.
- Use full country names, for example `Brazil`, not country codes like `BRA`.
- Each probability must be between `0` and `1`.
- For every row, `p_home_win + p_draw + p_away_win` must sum to `1`.
- Do not include the baseline helper column `predicted` in the upload file.

## Downloaded Sample

Downloaded sample path:

```text
C:\Users\aab\Downloads\sample-predictions.csv
```

WSL path:

```text
/mnt/c/Users/aab/Downloads/sample-predictions.csv
```

Sample contents:

```csv
date,home_team,away_team,p_home_win,p_draw,p_away_win
2026-06-28,Argentina,Nigeria,0.62,0.23,0.15
2026-06-28,Spain,Japan,0.55,0.27,0.18
2026-06-29,Brazil,South Korea,0.66,0.21,0.13
2026-06-29,France,Senegal,0.58,0.25,0.17
```

## Baseline Export Note

The current starter baseline writes:

```csv
date,home_team,away_team,predicted,p_home_win,p_draw,p_away_win
```

Before uploading, export only:

```csv
date,home_team,away_team,p_home_win,p_draw,p_away_win
```

Recommended output location:

```text
outputs/round_of_32_submission.csv
```

## Confirmed Fixtures

The full Round of 32 fixture list is stored in:

```text
data/processed/round_of_32_fixtures.csv
```

Current confirmed rows:

```csv
match_no,date,time_local,home_team,away_team,venue,city,country,neutral
73,2026-06-28,12:00,South Africa,Canada,SoFi Stadium,Inglewood,United States,TRUE
76,2026-06-29,12:00,Brazil,Japan,NRG Stadium,Houston,United States,TRUE
74,2026-06-29,16:30,Germany,Paraguay,Gillette Stadium,Foxborough,United States,TRUE
75,2026-06-29,19:00,Netherlands,Morocco,Estadio BBVA,Guadalupe,Mexico,TRUE
78,2026-06-30,12:00,Ivory Coast,Norway,AT&T Stadium,Arlington,United States,TRUE
77,2026-06-30,17:00,France,Sweden,MetLife Stadium,East Rutherford,United States,TRUE
79,2026-06-30,19:00,Mexico,Ecuador,Estadio Azteca,Mexico City,Mexico,FALSE
80,2026-07-01,12:00,England,DR Congo,Mercedes-Benz Stadium,Atlanta,United States,TRUE
82,2026-07-01,13:00,Belgium,Senegal,Lumen Field,Seattle,United States,TRUE
81,2026-07-01,17:00,United States,Bosnia and Herzegovina,Levi's Stadium,Santa Clara,United States,FALSE
84,2026-07-02,12:00,Spain,Austria,SoFi Stadium,Inglewood,United States,TRUE
83,2026-07-02,19:00,Portugal,Croatia,BMO Field,Toronto,Canada,TRUE
85,2026-07-02,20:00,Switzerland,Algeria,BC Place,Vancouver,Canada,TRUE
88,2026-07-03,13:00,Australia,Egypt,AT&T Stadium,Arlington,United States,TRUE
86,2026-07-03,18:00,Argentina,Cape Verde,Hard Rock Stadium,Miami Gardens,United States,TRUE
87,2026-07-03,20:30,Colombia,Ghana,Arrowhead Stadium,Kansas City,United States,TRUE
```

Source trail:

- The FIFA knockout-stage schedule defines match numbers, dates, local times, and venues.
- CBS Sports published the full confirmed Round of 32 bracket after group-stage completion.
- Sports Illustrated and Al Jazeera were used as cross-checks for fixture dates, times, and venues.

## Generating Round Output

Run from the repository root:

```bash
tabpfn-football-predictions/.venv/bin/python scripts/predict_custom_fixtures.py \
  data/processed/round_of_32_fixtures.csv \
  outputs/round_of_32_submission.csv
```

Generated upload file:

```text
outputs/round_of_32_submission.csv
```

## Validation Checklist

Before upload:

- Header exactly matches the required six columns.
- No `predicted` column.
- Country names are full names.
- No missing probabilities.
- No negative probabilities.
- No probabilities greater than `1`.
- Row probability sums are `1` within normal floating-point tolerance.
- Match dates and home/away teams match the competition round.
