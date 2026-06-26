#!/usr/bin/env python3
"""Export a baseline prediction CSV to the official round upload schema."""
import argparse
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "home_team",
    "away_team",
    "p_home_win",
    "p_draw",
    "p_away_win",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise SystemExit(f"Missing required columns: {', '.join(missing)}")

    out = df[REQUIRED_COLUMNS].copy()
    probs = out[["p_home_win", "p_draw", "p_away_win"]]

    if probs.isna().any().any():
        raise SystemExit("Probability columns contain missing values")
    if ((probs < 0) | (probs > 1)).any().any():
        raise SystemExit("Probability columns must be between 0 and 1")

    sums = probs.sum(axis=1)
    if not sums.between(0.999999, 1.000001).all():
        raise SystemExit("Probability columns must sum to 1 for every row")

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)
    print(f"Wrote {len(out)} rows to {args.output_csv}")


if __name__ == "__main__":
    main()
