#!/usr/bin/env python3
"""Predict custom fixtures with the starter TabPFN baseline."""
import argparse
import os
import sys
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
STARTER_DIR = REPO_ROOT / "tabpfn-football-predictions"
sys.path.insert(0, str(STARTER_DIR))

import predict  # noqa: E402


UPLOAD_COLUMNS = [
    "date",
    "home_team",
    "away_team",
    "p_home_win",
    "p_draw",
    "p_away_win",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixtures_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()

    fixtures = pd.read_csv(args.fixtures_csv)
    required = ["date", "home_team", "away_team", "city", "country", "neutral"]
    missing = [col for col in required if col not in fixtures.columns]
    if missing:
        raise SystemExit(f"Missing fixture columns: {', '.join(missing)}")

    original_cwd = Path.cwd()
    os.chdir(STARTER_DIR)
    try:
        df = predict.load_data(False)
    finally:
        os.chdir(original_cwd)
    custom = pd.DataFrame({
        "date": pd.to_datetime(fixtures["date"]),
        "home_team": fixtures["home_team"],
        "away_team": fixtures["away_team"],
        "home_score": float("nan"),
        "away_score": float("nan"),
        "tournament": "FIFA World Cup",
        "city": fixtures["city"],
        "country": fixtures["country"],
        "neutral": fixtures["neutral"].astype(str).str.upper().eq("TRUE").astype(int),
    })
    custom["outcome"] = float("nan")
    custom["importance"] = custom["tournament"].apply(predict.importance)

    combined = pd.concat([df, custom], ignore_index=True).sort_values("date").reset_index(drop=True)
    feats = predict.build_features(combined)
    played = feats[feats["outcome"].notna() & (feats["date"] >= predict.TRAIN_START)]

    fixture_keys = set(zip(custom["date"], custom["home_team"], custom["away_team"]))
    target = feats[
        feats.apply(lambda r: (r["date"], r["home_team"], r["away_team"]) in fixture_keys, axis=1)
        & feats["home_score"].isna()
    ].copy()
    target["_order"] = target.apply(
        lambda r: fixtures.index[
            (pd.to_datetime(fixtures["date"]) == r["date"])
            & (fixtures["home_team"] == r["home_team"])
            & (fixtures["away_team"] == r["away_team"])
        ][0],
        axis=1,
    )
    target = target.sort_values("_order")

    clf = predict.train(played.tail(predict.MAX_TRAIN))
    proba = clf.predict_proba(target[predict.FEATURES].values)
    cols = {cls: proba[:, i] for i, cls in enumerate(clf.classes_)}

    out = target[["date", "home_team", "away_team"]].copy()
    out["p_home_win"] = cols["home_win"]
    out["p_draw"] = cols["draw"]
    out["p_away_win"] = cols["away_win"]
    out["date"] = out["date"].dt.strftime("%Y-%m-%d")

    prob_cols = ["p_home_win", "p_draw", "p_away_win"]
    out[prob_cols] = out[prob_cols].div(out[prob_cols].sum(axis=1), axis=0)
    out = out[UPLOAD_COLUMNS]

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)
    print(f"Wrote {len(out)} rows to {args.output_csv}")


if __name__ == "__main__":
    main()
