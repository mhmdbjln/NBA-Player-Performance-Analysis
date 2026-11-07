# NBA Player Performance Analysis (2000–2009)

A Python data-analysis project exploring NBA player statistics across the 2000–2009 seasons. The analysis uses **Pandas** to filter player-season records, calculate a custom player-value score, and identify the highest-scoring team in each season.

> **Dataset note:** The original `NBA2000-2009.csv` input file was not included in the supplied project archive. The repository contains the analysis code and the three CSV result files supplied with the project. To reproduce the analysis, obtain the source dataset separately, verify its redistribution terms, and place it in `data/NBA2000-2009.csv`.

## Analyses

### 1. Player-seasons with multiple double-digit averages

Combines offensive and defensive rebounds into `REB`, then selects player-season records with at least two of the following five averages greater than or equal to 10:

- Points (`PTS`)
- Assists (`AST`)
- Rebounds (`REB`)
- Steals (`STL`)
- Blocks (`BLK`)

The result is sorted by season and player name.

### 2. Player value ranking

Calculates a custom season score:

```text
(PTS + OREB + DREB + AST + STL + BLK)
- (TOV + Missed FG + Missed FT)
```

where `Missed FG = FGA - FGM` and `Missed FT = FTA - FTM`. The project then averages this score across the available seasons for each player and ranks players by the resulting value.

This is a project-defined statistical score, not an official NBA metric.

### 3. Top-scoring team by season

Sums the player scoring averages (`PTS`) for each team in each season and selects the team with the highest total for that season.

## Repository structure

```text
.
├── data/
│   └── README.md
├── notebooks/
│   └── NBA_Analysis.ipynb
├── outputs/
│   ├── best_player.csv
│   ├── double_double.csv
│   └── max_PTS_of_year.csv
├── nba_analysis.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.9 or newer
- Pandas

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
```

## Run

Place the source file at `data/NBA2000-2009.csv`, then run:

```bash
python nba_analysis.py
```

To specify a different input path or output directory:

```bash
python nba_analysis.py --input path/to/NBA2000-2009.csv --output-dir outputs
```

The script writes:

- `outputs/double_double.csv`
- `outputs/best_player.csv`
- `outputs/max_PTS_of_year.csv`

## Notebook

An optional Jupyter notebook is available at `notebooks/NBA_Analysis.ipynb`. Install Jupyter separately with `pip install notebook`, then launch it from the repository root with `jupyter notebook`. The notebook calls the same functions as the Python script.

## Included result files

The `outputs/` directory contains the result CSV files supplied with the original project archive. They are provided as reference outputs; the original input dataset was not included, so these files have not been independently regenerated from the raw source data in this repository.

## Limitations

- The player-value formula is a custom scoring rule defined for this analysis. It should not be interpreted as an official measure of player quality.
- The analysis aggregates season-level player averages as specified in the original project; it does not normalize by games played or playing time.
- Results are limited to the data represented in the source dataset.

## License and data provenance

No software license has been specified. The original source dataset was not supplied with the project. Confirm its provenance and redistribution terms before adding it to this repository.
