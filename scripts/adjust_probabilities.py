#!/usr/bin/env python3
"""Apply deterministic feature adjustments and market blending to outcome probabilities."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd


PROB_COLS = ["p_home_win", "p_draw", "p_away_win"]
OUTPUT_COLS = ["date", "home_team", "away_team", *PROB_COLS]


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    sums = df[PROB_COLS].sum(axis=1)
    df[PROB_COLS] = df[PROB_COLS].div(sums, axis=0)
    return df


def apply_edge(df: pd.DataFrame, edge: pd.Series, strength: float, label: str) -> None:
    """Move probability toward home or away without directly touching draw."""
    if strength == 0:
        return
    factor = np.exp(edge.fillna(0.0) * strength)
    df["p_home_win"] *= factor
    df["p_away_win"] /= factor
    df[f"adj_{label}"] = edge.fillna(0.0)


def apply_uniform_shrink(df: pd.DataFrame, amount: pd.Series, label: str) -> None:
    """Increase uncertainty by moving probabilities slightly toward 1/3."""
    amount = amount.clip(lower=0.0, upper=0.2).fillna(0.0)
    for col in PROB_COLS:
        df[col] = df[col] * (1.0 - amount) + (1.0 / 3.0) * amount
    df[f"adj_{label}"] = amount


def add_team_context(fixtures: pd.DataFrame, context: pd.DataFrame) -> pd.DataFrame:
    home = context.add_prefix("home_").rename(columns={"home_team": "home_team"})
    away = context.add_prefix("away_").rename(columns={"away_team": "away_team"})
    out = fixtures.merge(home, on="home_team", how="left")
    out = out.merge(away, on="away_team", how="left")
    return out


def market_probabilities(odds: pd.DataFrame) -> pd.DataFrame:
    odds = odds.dropna(subset=["home_odds", "draw_odds", "away_odds"]).copy()
    if odds.empty:
        return pd.DataFrame(columns=["match_no", "market_home", "market_draw", "market_away"])

    for col in ["home_odds", "draw_odds", "away_odds"]:
        odds[col] = pd.to_numeric(odds[col], errors="coerce")
    odds = odds.dropna(subset=["home_odds", "draw_odds", "away_odds"])
    odds = odds[(odds["home_odds"] > 1) & (odds["draw_odds"] > 1) & (odds["away_odds"] > 1)]

    raw = pd.DataFrame({
        "match_no": odds["match_no"],
        "market_home": 1.0 / odds["home_odds"],
        "market_draw": 1.0 / odds["draw_odds"],
        "market_away": 1.0 / odds["away_odds"],
    })
    raw[["market_home", "market_draw", "market_away"]] = raw[
        ["market_home", "market_draw", "market_away"]
    ].div(raw[["market_home", "market_draw", "market_away"]].sum(axis=1), axis=0)

    return raw.groupby("match_no", as_index=False)[
        ["market_home", "market_draw", "market_away"]
    ].median()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_probabilities_csv", type=Path)
    parser.add_argument("fixtures_csv", type=Path)
    parser.add_argument("team_context_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--market-odds-csv", type=Path)
    parser.add_argument("--group-points-weight", type=float, default=0.025)
    parser.add_argument("--group-goal-diff-weight", type=float, default=0.035)
    parser.add_argument("--prior-run-weight", type=float, default=0.020)
    parser.add_argument("--host-weight", type=float, default=0.060)
    parser.add_argument("--cross-confed-uncertainty", type=float, default=0.015)
    parser.add_argument("--market-weight", type=float, default=0.35)
    args = parser.parse_args()

    base = pd.read_csv(args.base_probabilities_csv)
    fixtures = pd.read_csv(args.fixtures_csv)
    context = pd.read_csv(args.team_context_csv)

    missing = [col for col in OUTPUT_COLS if col not in base.columns]
    if missing:
        raise SystemExit(f"Missing probability columns: {', '.join(missing)}")

    merged = fixtures.merge(base, on=["date", "home_team", "away_team"], how="left")
    if merged[PROB_COLS].isna().any().any():
        raise SystemExit("Base probabilities do not cover every fixture row")

    df = add_team_context(merged, context)

    for col in [
        "home_group_points", "away_group_points",
        "home_group_goal_diff", "away_group_goal_diff",
        "home_prior_run_score", "away_prior_run_score",
    ]:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    apply_edge(
        df,
        df["home_group_points"] - df["away_group_points"],
        args.group_points_weight,
        "group_points_diff",
    )
    apply_edge(
        df,
        df["home_group_goal_diff"] - df["away_group_goal_diff"],
        args.group_goal_diff_weight,
        "group_goal_diff_diff",
    )
    apply_edge(
        df,
        df["home_prior_run_score"] - df["away_prior_run_score"],
        args.prior_run_weight,
        "prior_run_diff",
    )

    home_host = df["home_is_host"].astype(str).str.upper().eq("TRUE")
    away_host = df["away_is_host"].astype(str).str.upper().eq("TRUE")
    venue_home = df["country"].eq(df["home_team"])
    venue_away = df["country"].eq(df["away_team"])
    apply_edge(df, (home_host & venue_home).astype(float) - (away_host & venue_away).astype(float), args.host_weight, "host_edge")

    cross_confed = ~df["home_confederation"].eq(df["away_confederation"])
    apply_uniform_shrink(df, pd.Series(args.cross_confed_uncertainty, index=df.index).where(cross_confed, 0.0), "cross_confed_uncertainty")

    normalize(df)

    if args.market_odds_csv:
        market = market_probabilities(pd.read_csv(args.market_odds_csv))
        if not market.empty:
            df = df.merge(market, on="match_no", how="left")
            has_market = df[["market_home", "market_draw", "market_away"]].notna().all(axis=1)
            w = args.market_weight
            df.loc[has_market, "p_home_win"] = (
                (1 - w) * df.loc[has_market, "p_home_win"] + w * df.loc[has_market, "market_home"]
            )
            df.loc[has_market, "p_draw"] = (
                (1 - w) * df.loc[has_market, "p_draw"] + w * df.loc[has_market, "market_draw"]
            )
            df.loc[has_market, "p_away_win"] = (
                (1 - w) * df.loc[has_market, "p_away_win"] + w * df.loc[has_market, "market_away"]
            )
            df["adj_market_blend"] = has_market.astype(float) * w
            normalize(df)

    out = df[OUTPUT_COLS]
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)

    diagnostics = [col for col in df.columns if col.startswith("adj_")]
    if diagnostics:
        diag_path = args.output_csv.with_name(args.output_csv.stem + "_diagnostics.csv")
        df[["match_no", "date", "home_team", "away_team", *diagnostics]].to_csv(diag_path, index=False)
        print(f"Wrote diagnostics to {diag_path}")

    print(f"Wrote {len(out)} rows to {args.output_csv}")


if __name__ == "__main__":
    main()
