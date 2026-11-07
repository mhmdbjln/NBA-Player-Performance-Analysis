"""Analyze NBA player statistics for the 2000-2009 seasons.

Expected input columns:
    PLAYER, TEAM, YEAR, PTS, FGM, FGA, FTM, FTA,
    OREB, DREB, AST, STL, BLK, TOV

The script writes three CSV reports to the selected output directory.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "PLAYER",
    "TEAM",
    "YEAR",
    "PTS",
    "FGM",
    "FGA",
    "FTM",
    "FTA",
    "OREB",
    "DREB",
    "AST",
    "STL",
    "BLK",
    "TOV",
}


def load_nba_data(input_path: Path) -> pd.DataFrame:
    """Load the source dataset and validate its required columns."""
    if not input_path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {input_path}\n"
            "Place NBA2000-2009.csv in the data/ directory or pass --input."
        )

    data = pd.read_csv(input_path)
    missing = sorted(REQUIRED_COLUMNS.difference(data.columns))
    if missing:
        raise ValueError(
            "The input dataset is missing required columns: " + ", ".join(missing)
        )

    return data.copy()


def find_double_digit_performances(data: pd.DataFrame) -> pd.DataFrame:
    """Find player-seasons with at least two of five averages >= 10."""
    result = data.copy()
    result["REB"] = result["OREB"] + result["DREB"]
    stats = ["PTS", "AST", "REB", "STL", "BLK"]

    qualifies = (result[stats] >= 10).sum(axis=1) >= 2
    result = result.loc[qualifies, ["PLAYER", "YEAR", *stats]]
    return result.sort_values(["YEAR", "PLAYER"], ascending=[True, True])


def rank_players_by_value(data: pd.DataFrame) -> pd.DataFrame:
    """Rank players by mean season value using the project's scoring formula."""
    result = data.copy()
    result["MISSED_FG"] = (result["FGA"] - result["FGM"]).round(2)
    result["MISSED_FT"] = (result["FTA"] - result["FTM"]).round(2)

    positive_stats = result[["PTS", "OREB", "DREB", "AST", "STL", "BLK"]].sum(axis=1)
    negative_stats = result[["TOV", "MISSED_FG", "MISSED_FT"]].sum(axis=1)
    result["VALUE"] = (positive_stats - negative_stats).round(2)

    ranking = result.groupby("PLAYER", as_index=False)["VALUE"].mean()
    ranking["VALUE"] = ranking["VALUE"].round(2)
    return ranking.sort_values(
        ["VALUE", "PLAYER"], ascending=[False, True]
    ).reset_index(drop=True)


def find_top_scoring_team_by_year(data: pd.DataFrame) -> pd.DataFrame:
    """Find the team with the largest sum of player scoring averages per year."""
    totals = (
        data.groupby(["YEAR", "TEAM"], as_index=False)["PTS"]
        .sum()
        .rename(columns={"PTS": "PTS"})
    )
    totals["PTS"] = totals["PTS"].round(2)
    best_rows = totals.groupby("YEAR")["PTS"].idxmax()
    return (
        totals.loc[best_rows, ["YEAR", "TEAM", "PTS"]]
        .sort_values("YEAR")
        .reset_index(drop=True)
    )


def analyze_nba(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run all three analyses and return their result DataFrames."""
    double_double = find_double_digit_performances(data)
    best_player = rank_players_by_value(data)
    max_pts_of_year = find_top_scoring_team_by_year(data)
    return double_double, best_player, max_pts_of_year


def save_results(
    results: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame], output_dir: Path
) -> None:
    """Save analysis results as CSV files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    filenames = ["double_double.csv", "best_player.csv", "max_PTS_of_year.csv"]

    for dataframe, filename in zip(results, filenames):
        dataframe.to_csv(output_dir / filename, index=False)
        print(f"Saved: {output_dir / filename} ({len(dataframe)} rows)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze NBA player statistics from the 2000-2009 seasons."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/NBA2000-2009.csv"),
        help="Path to the source NBA CSV dataset (default: data/NBA2000-2009.csv).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory for generated CSV reports (default: outputs/).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = load_nba_data(args.input)
    results = analyze_nba(data)
    save_results(results, args.output_dir)


if __name__ == "__main__":
    main()
