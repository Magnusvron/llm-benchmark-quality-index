"""
BQAI Score Computation
=======================

Computes BQAI scores and tier assignments from reconciled per-dimension scores.

Formula:
    BQAI = 0.349·Q4 + 0.213·Q1 + 0.167·Q5 + 0.117·Q3 + 0.073·Q2 + 0.048·Q7 + 0.033·Q6

Weights are derived via AHP (see ahp_weights.py).

Tier classification:
    Tier A: BQAI ≥ 0.82
    Tier B: 0.70 ≤ BQAI < 0.82
    Tier C: BQAI < 0.70

Usage:
    # Default: read reconciled scores from 02_scoring/reconciled_scores.csv
    python compute_bqai.py

    # Custom input/output paths
    python compute_bqai.py --input my_scores.csv --output my_results.csv

    # Use custom weights (for sensitivity analysis or alternative schemes)
    python compute_bqai.py --weights alternative_weights.json
"""

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

# Default weights (from AHP derivation in ahp_weights.py)
DEFAULT_WEIGHTS = {
    "Q1": 0.213,
    "Q2": 0.073,
    "Q3": 0.117,
    "Q4": 0.349,
    "Q5": 0.167,
    "Q6": 0.033,
    "Q7": 0.048,
}

# Tier thresholds (from paper §6.3)
TIER_A_THRESHOLD = 0.82
TIER_B_THRESHOLD = 0.70

DIMENSIONS = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"]


def load_weights(path: Path | None) -> dict[str, float]:
    """Load weights from JSON file, or return defaults."""
    if path is None:
        return DEFAULT_WEIGHTS.copy()
    if not path.exists():
        sys.exit(f"Weights file not found: {path}")
    data = json.loads(path.read_text())
    # Accept either {"weights": {...}} or flat {...}
    weights = data.get("weights", data)
    # Validate
    missing = [q for q in DIMENSIONS if q not in weights]
    if missing:
        sys.exit(f"Weights file missing dimensions: {missing}")
    # Normalize to sum to 1 (safety)
    total = sum(weights[q] for q in DIMENSIONS)
    if abs(total - 1.0) > 0.01:
        print(f"Warning: weights sum to {total:.4f}, normalizing to 1.0")
        weights = {q: weights[q] / total for q in DIMENSIONS}
    return {q: float(weights[q]) for q in DIMENSIONS}


def load_scores(path: Path) -> pd.DataFrame:
    """Load per-benchmark, per-dimension scores from CSV.

    Expected columns: benchmark, Q1, Q2, Q3, Q4, Q5, Q6, Q7
    Optional columns: dimension (primary), track, year, notes
    """
    if not path.exists():
        sys.exit(
            f"Scores file not found: {path}\n"
            f"Expected CSV with columns: benchmark, Q1, Q2, Q3, Q4, Q5, Q6, Q7"
        )
    df = pd.read_csv(path)
    missing = [c for c in ["benchmark"] + DIMENSIONS if c not in df.columns]
    if missing:
        sys.exit(f"Scores file missing columns: {missing}")
    # Coerce numeric for Q-columns
    for q in DIMENSIONS:
        df[q] = pd.to_numeric(df[q], errors="coerce")
    return df


def compute_bqai(scores: pd.DataFrame, weights: dict[str, float]) -> pd.DataFrame:
    """Add BQAI and Tier columns to the scores DataFrame."""
    df = scores.copy()
    df["BQAI"] = sum(df[q] * weights[q] for q in DIMENSIONS)
    df["Tier"] = df["BQAI"].apply(_assign_tier)
    return df


def _assign_tier(bqai: float) -> str:
    if pd.isna(bqai):
        return "—"
    if bqai >= TIER_A_THRESHOLD:
        return "A"
    if bqai >= TIER_B_THRESHOLD:
        return "B"
    return "C"


def print_report(df: pd.DataFrame, weights: dict[str, float]) -> None:
    """Print human-readable BQAI report sorted by score."""
    print("=" * 72)
    print("BQAI COMPUTATION RESULTS")
    print("=" * 72)
    print()
    print("Weights used:")
    for q in DIMENSIONS:
        print(f"  {q}: {weights[q]:.4f}")
    print()
    print("-" * 72)
    print("Results (sorted by BQAI, descending):")
    print("-" * 72)
    print(f"  {'#':<4}{'Benchmark':<22}{'BQAI':>8}  {'Tier':<6}")
    print("  " + "-" * 38)
    df_sorted = df.sort_values("BQAI", ascending=False).reset_index(drop=True)
    for i, row in df_sorted.iterrows():
        tier_marker = {"A": "✓", "B": " ", "C": "!"}.get(row["Tier"], " ")
        print(f"  {i+1:<4}{row['benchmark']:<22}{row['BQAI']:>8.3f}  {row['Tier']:<3}{tier_marker}")
    print()
    print("-" * 72)
    print("Tier summary:")
    print("-" * 72)
    counts = df["Tier"].value_counts().sort_index()
    for tier in ["A", "B", "C"]:
        n = counts.get(tier, 0)
        threshold_text = {
            "A": f"BQAI ≥ {TIER_A_THRESHOLD}",
            "B": f"{TIER_B_THRESHOLD} ≤ BQAI < {TIER_A_THRESHOLD}",
            "C": f"BQAI < {TIER_B_THRESHOLD}",
        }[tier]
        print(f"  Tier {tier} ({threshold_text}): {n} benchmarks")
    total = sum(counts.get(t, 0) for t in ["A", "B", "C"])
    print(f"  Total: {total} benchmarks")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute BQAI scores from per-dimension data")
    parser.add_argument(
        "--input", type=Path,
        default=Path(__file__).parent.parent / "02_scoring" / "reconciled_scores.csv",
        help="Path to reconciled scores CSV (default: 02_scoring/reconciled_scores.csv)"
    )
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).parent / "bqai_results.csv",
        help="Output path for results CSV (default: 04_bqai/bqai_results.csv)"
    )
    parser.add_argument(
        "--weights", type=Path, default=None,
        help="Optional JSON file with custom weights (default: AHP-derived)"
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress console report (still writes output CSV)"
    )
    args = parser.parse_args()

    weights = load_weights(args.weights)
    scores = load_scores(args.input)
    results = compute_bqai(scores, weights)

    if not args.quiet:
        print_report(results, weights)

    # Write output
    results.to_csv(args.output, index=False, float_format="%.4f")
    if not args.quiet:
        print(f"Results written to: {args.output}")


if __name__ == "__main__":
    main()
