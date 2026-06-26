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

Known Round of 32 fixtures are stored in:

```text
data/processed/round_of_32_known_fixtures.csv
```

Current confirmed rows:

```csv
match_no,date,time_local,home_team,away_team,venue,city,country,neutral
73,2026-06-28,12:00,South Africa,Canada,SoFi Stadium,Inglewood,United States,TRUE
76,2026-06-29,12:00,Brazil,Japan,NRG Stadium,Houston,United States,TRUE
75,2026-06-29,19:00,Netherlands,Morocco,Estadio BBVA,Guadalupe,Mexico,TRUE
81,2026-07-01,17:00,United States,Bosnia and Herzegovina,Levi's Stadium,Santa Clara,United States,FALSE
```

Source trail:

- The Round of 32 bracket confirms Match 73 South Africa vs Canada, Match 75 Netherlands vs Morocco, Match 76 Brazil vs Japan, and Match 81 United States vs Bosnia and Herzegovina.
- The match schedule gives the exact date, local time, and venue for those match numbers.
- The schedule references FIFA match reports for those four confirmed matches.

## Generating Known-Fixture Output

Run from the repository root:

```bash
tabpfn-football-predictions/.venv/bin/python scripts/predict_custom_fixtures.py \
  data/processed/round_of_32_known_fixtures.csv \
  outputs/round_of_32_known_fixtures_submission_20260626.csv
```

Generated upload file:

```text
outputs/round_of_32_known_fixtures_submission_20260626.csv
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
