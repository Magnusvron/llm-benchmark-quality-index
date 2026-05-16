"""
Inter-Rater Reliability Analysis for BQAI Scoring
===================================================

Reads the three independent evaluators' scoring spreadsheets and computes
formal IAA metrics:

  - ICC(2,k)  : Intraclass Correlation Coefficient, two-way random effects,
                average of k raters, absolute agreement. Appropriate for
                continuous scores with random raters.
  - ICC(2,1)  : Single-rater version of the above (more conservative).
  - Weighted κ: Quadratic-weighted Cohen's kappa, computed pairwise after
                binning scores into the four tiers (Low/Mod/High/Excellent).
  - Pearson / Spearman correlations per rater pair.
  - Mean absolute difference (for continuity with paper's prior 0.07 figure).

Interpretation:
  ICC(2,k):  <0.50 poor | 0.50-0.74 moderate | 0.75-0.90 good | >0.90 excellent
  Weighted κ: <0.40 weak | 0.40-0.59 moderate | 0.60-0.79 substantial | ≥0.80 strong

Usage:
    # Default: read filled Excel files from 02_scoring/raw_scores/
    python compute_iaa.py

    # Custom input directory
    python compute_iaa.py --input-dir path/to/raw_scores/

Inputs expected:
    raw_scores/BQAI_scoring_<Name1>.xlsx
    raw_scores/BQAI_scoring_<Name2>.xlsx
    raw_scores/BQAI_scoring_<Name3>.xlsx
    (Generated from BQAI_scoring_template_ES.xlsx in docs/)

Outputs:
    - Console summary with all IAA metrics
    - iaa_results.json : machine-readable
    - iaa_report.md    : human-readable, includes suggested manuscript text
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import pingouin as pg
    HAS_PINGOUIN = True
except ImportError:
    HAS_PINGOUIN = False

from scipy.stats import pearsonr, spearmanr

try:
    from sklearn.metrics import cohen_kappa_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


DIMENSIONS = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"]


# ============================================================
# Excel parsing — robust to template format
# ============================================================
def find_scoring_excels(input_dir: Path) -> list[Path]:
    """Find all BQAI_scoring_*.xlsx files in the input directory."""
    files = sorted(input_dir.glob("BQAI_scoring_*.xlsx"))
    if not files:
        sys.exit(
            f"No scoring Excel files found in {input_dir}\n"
            f"Expected filenames: BQAI_scoring_<EvaluatorName>.xlsx"
        )
    return files


def parse_evaluator_excel(path: Path) -> pd.DataFrame:
    """Parse one evaluator's Excel file into a long-format DataFrame.

    Returns columns: benchmark, Q1, Q2, Q3, Q4, Q5, Q6, Q7, evaluator
    """
    # Load the 'Scoring' sheet
    sheet_candidates = ["Scoring", "scoring"]
    for sheet in sheet_candidates:
        try:
            # Header is at row 6 (1-indexed) in the template = index 5
            df = pd.read_excel(path, sheet_name=sheet, header=5, engine="openpyxl")
            break
        except Exception:
            continue
    else:
        sys.exit(f"Could not find 'Scoring' sheet in {path}")

    # Normalize column names: 'Q1\n(0.213)' -> 'Q1', etc.
    rename_map = {}
    for col in df.columns:
        col_str = str(col).strip()
        for q in DIMENSIONS:
            if col_str.startswith(q):
                rename_map[col] = q
                break
        if col_str == "Benchmark":
            rename_map[col] = "benchmark"
    df = df.rename(columns=rename_map)

    # Validate
    needed = ["benchmark"] + DIMENSIONS
    missing = [c for c in needed if c not in df.columns]
    if missing:
        sys.exit(f"{path.name}: missing columns {missing}.\nGot: {list(df.columns)}")

    # Keep only valid benchmark rows (drop section dividers and empty rows)
    df = df[df["benchmark"].notna()].copy()
    # Drop rows where benchmark is non-string (e.g., NaN slip-throughs)
    df = df[df["benchmark"].apply(lambda x: isinstance(x, str))]
    # Drop rows where ALL Q values are NaN (likely section dividers)
    df = df[df[DIMENSIONS].notna().any(axis=1)]

    # Coerce Q columns to numeric
    for q in DIMENSIONS:
        df[q] = pd.to_numeric(df[q], errors="coerce")

    # Add evaluator label from filename
    evaluator = path.stem.replace("BQAI_scoring_", "")
    df["evaluator"] = evaluator

    return df[["benchmark"] + DIMENSIONS + ["evaluator"]].reset_index(drop=True)


def build_long_table(input_dir: Path) -> pd.DataFrame:
    """Load all evaluator files and concatenate into a long table."""
    files = find_scoring_excels(input_dir)
    frames = [parse_evaluator_excel(p) for p in files]
    long = pd.concat(frames, ignore_index=True)
    print(f"Loaded {len(frames)} evaluator files: "
          f"{', '.join(sorted(long['evaluator'].unique()))}")
    print(f"Total rows: {len(long)}, unique benchmarks: {long['benchmark'].nunique()}\n")
    return long


# ============================================================
# IAA metric computations
# ============================================================
def compute_icc(long_df: pd.DataFrame, q: str) -> dict:
    """Compute ICC(2,k) and ICC(2,1) for dimension q.

    ICC(2,k) = two-way random effects, absolute agreement, k raters average.
    Pingouin labels this 'ICC(A,k)' in version >=0.5.
    """
    sub = long_df[["benchmark", "evaluator", q]].dropna()
    if HAS_PINGOUIN:
        try:
            icc = pg.intraclass_corr(
                data=sub, targets="benchmark", raters="evaluator", ratings=q,
                nan_policy="omit",
            )
            # Handle both old and new pingouin API
            ci_col = "CI95" if "CI95" in icc.columns else "CI95%"
            row_k = icc[icc["Type"].isin(["ICC(A,k)", "ICC2k"])].iloc[0]
            row_1 = icc[icc["Type"].isin(["ICC(A,1)", "ICC2"])].iloc[0]
            return {
                "ICC2k": float(row_k["ICC"]),
                "ICC2k_CI": [float(row_k[ci_col][0]), float(row_k[ci_col][1])],
                "ICC21": float(row_1["ICC"]),
                "ICC21_CI": [float(row_1[ci_col][0]), float(row_1[ci_col][1])],
                "F": float(row_k["F"]),
                "p": float(row_k["pval"]),
            }
        except Exception as e:
            return {"error": f"pingouin ICC failed: {e}", "ICC2k": None, "ICC21": None}
    return _icc_manual(sub, q)


def _icc_manual(sub: pd.DataFrame, q: str) -> dict:
    """Manual ICC(2,k) via variance components, used when pingouin unavailable."""
    wide = sub.pivot_table(index="benchmark", columns="evaluator", values=q).dropna()
    n, k = wide.shape
    if n < 2 or k < 2:
        return {"error": "Not enough data for ICC", "ICC2k": None, "ICC21": None}
    grand = wide.values.mean()
    ss_total = ((wide.values - grand) ** 2).sum()
    ss_rows = k * ((wide.mean(axis=1) - grand) ** 2).sum()
    ss_cols = n * ((wide.mean(axis=0) - grand) ** 2).sum()
    ss_err = ss_total - ss_rows - ss_cols
    ms_rows = ss_rows / (n - 1)
    ms_cols = ss_cols / (k - 1)
    ms_err = ss_err / ((n - 1) * (k - 1)) if (n - 1) * (k - 1) > 0 else 0.0
    if ms_err == 0:
        return {"error": "Zero error variance", "ICC2k": None, "ICC21": None}
    icc2k = (ms_rows - ms_err) / (ms_rows + (ms_cols - ms_err) / n)
    icc21 = (ms_rows - ms_err) / (
        ms_rows + (k - 1) * ms_err + k * (ms_cols - ms_err) / n
    )
    return {
        "ICC2k": float(icc2k), "ICC21": float(icc21),
        "ICC2k_CI": None, "ICC21_CI": None, "F": None, "p": None,
    }


def cohen_kappa_weighted(long_df: pd.DataFrame, q: str) -> dict:
    """Average pairwise quadratic-weighted Cohen's κ for dimension q.

    Scores are binned into 4 ordinal tiers before kappa.
    """
    if not HAS_SKLEARN:
        return {"avg_weighted_kappa": None, "pairs": [],
                "error": "scikit-learn not installed"}

    def bin_tier(x):
        if pd.isna(x):
            return np.nan
        if x <= 0.30:
            return 0
        if x <= 0.60:
            return 1
        if x <= 0.80:
            return 2
        return 3

    wide = long_df.pivot_table(index="benchmark", columns="evaluator", values=q)
    # pandas >=2.1 uses .map; older uses .applymap
    try:
        binned = wide.map(bin_tier)
    except AttributeError:
        binned = wide.applymap(bin_tier)

    raters = list(binned.columns)
    pair_kappas = []
    for i in range(len(raters)):
        for j in range(i + 1, len(raters)):
            a = binned[raters[i]]
            b = binned[raters[j]]
            mask = a.notna() & b.notna()
            if mask.sum() < 2:
                continue
            try:
                k = cohen_kappa_score(
                    a[mask].astype(int), b[mask].astype(int),
                    weights="quadratic",
                )
                pair_kappas.append([raters[i], raters[j], float(k)])
            except ValueError:
                # Can happen if all values are identical (no variance)
                pair_kappas.append([raters[i], raters[j], None])

    valid = [k for *_, k in pair_kappas if k is not None]
    avg = float(np.mean(valid)) if valid else None
    return {"avg_weighted_kappa": avg, "pairs": pair_kappas}


def pairwise_correlations(long_df: pd.DataFrame, q: str) -> list[dict]:
    """Pearson and Spearman correlations between all rater pairs."""
    wide = long_df.pivot_table(index="benchmark", columns="evaluator", values=q)
    raters = list(wide.columns)
    out = []
    for i in range(len(raters)):
        for j in range(i + 1, len(raters)):
            a = wide[raters[i]]
            b = wide[raters[j]]
            mask = a.notna() & b.notna()
            if mask.sum() < 3:
                continue
            try:
                r_p, p_p = pearsonr(a[mask], b[mask])
                r_s, p_s = spearmanr(a[mask], b[mask])
                out.append({
                    "rater_a": raters[i], "rater_b": raters[j],
                    "pearson_r": float(r_p), "pearson_p": float(p_p),
                    "spearman_r": float(r_s), "spearman_p": float(p_s),
                    "n": int(mask.sum()),
                })
            except Exception:
                continue
    return out


def mean_abs_diff(long_df: pd.DataFrame, q: str) -> float:
    """Average absolute pairwise difference (paper's prior 0.07 metric)."""
    wide = long_df.pivot_table(index="benchmark", columns="evaluator", values=q)
    raters = list(wide.columns)
    diffs = []
    for i in range(len(raters)):
        for j in range(i + 1, len(raters)):
            a = wide[raters[i]]
            b = wide[raters[j]]
            mask = a.notna() & b.notna()
            diffs.extend(np.abs(a[mask] - b[mask]).tolist())
    return float(np.mean(diffs)) if diffs else float("nan")


# ============================================================
# Reconciliation
# ============================================================
def reconcile_mean(long_df: pd.DataFrame) -> pd.DataFrame:
    """Mean across evaluators per (benchmark, dimension)."""
    return long_df.groupby("benchmark", as_index=False)[DIMENSIONS].mean()


# ============================================================
# Report generation
# ============================================================
def interpret_icc(icc: float | None) -> str:
    if icc is None:
        return "n/a"
    if icc < 0.50:
        return "poor"
    if icc < 0.75:
        return "moderate"
    if icc < 0.90:
        return "good"
    return "excellent"


def interpret_kappa(k: float | None) -> str:
    if k is None:
        return "n/a"
    if k < 0.40:
        return "weak"
    if k < 0.60:
        return "moderate"
    if k < 0.80:
        return "substantial"
    return "strong"


def build_text_report(results: dict, long_df: pd.DataFrame) -> str:
    """Build the human-readable Markdown report."""
    lines = []
    add = lines.append
    add("# BQAI Inter-Rater Reliability Report\n")
    add(f"**Evaluators (n={len(results['evaluators'])}):** "
        f"{', '.join(results['evaluators'])}")
    add(f"**Benchmarks scored:** {results['n_benchmarks']}")
    add(f"**Dimensions:** {', '.join(DIMENSIONS)}\n")

    add("## Per-dimension IAA metrics\n")
    add("| Dim | ICC(2,k) | 95% CI | Interpretation | Weighted κ | Interpretation | Mean \\|Δ\\| |")
    add("|-----|----------|--------|----------------|------------|----------------|-----------|")
    for q in DIMENSIONS:
        d = results["per_dimension"][q]
        icc = d["icc"].get("ICC2k")
        ci = d["icc"].get("ICC2k_CI")
        ci_str = f"[{ci[0]:.2f}, {ci[1]:.2f}]" if ci else "n/a"
        kappa = d["weighted_kappa"]["avg_weighted_kappa"]
        mad = d["mean_abs_diff"]
        icc_str = f"{icc:.3f}" if icc is not None else "n/a"
        k_str = f"{kappa:.3f}" if kappa is not None else "n/a"
        add(
            f"| {q} | {icc_str} | {ci_str} | {interpret_icc(icc)} | "
            f"{k_str} | {interpret_kappa(kappa)} | {mad:.3f} |"
        )

    add("\n## Aggregate metrics\n")
    valid_iccs = [results["per_dimension"][q]["icc"].get("ICC2k")
                  for q in DIMENSIONS]
    valid_iccs = [v for v in valid_iccs if v is not None]
    valid_kappas = [results["per_dimension"][q]["weighted_kappa"]["avg_weighted_kappa"]
                    for q in DIMENSIONS]
    valid_kappas = [v for v in valid_kappas if v is not None]
    if valid_iccs:
        add(f"- **Mean ICC(2,k):** {np.mean(valid_iccs):.3f} "
            f"(range {min(valid_iccs):.3f} – {max(valid_iccs):.3f}) → "
            f"**{interpret_icc(np.mean(valid_iccs))}** agreement")
    if valid_kappas:
        add(f"- **Mean weighted κ:** {np.mean(valid_kappas):.3f} "
            f"(range {min(valid_kappas):.3f} – {max(valid_kappas):.3f}) → "
            f"**{interpret_kappa(np.mean(valid_kappas))}** agreement")

    add("\n## Interpretation guide\n")
    add("| Metric | Poor | Moderate | Good/Substantial | Excellent/Strong |")
    add("|--------|------|----------|------------------|------------------|")
    add("| ICC(2,k) | <0.50 | 0.50–0.74 | 0.75–0.90 | >0.90 |")
    add("| Weighted κ | <0.40 | 0.40–0.59 | 0.60–0.79 | ≥0.80 |")

    add("\n## Suggested manuscript text (§7.1)\n")
    if valid_iccs and valid_kappas and HAS_PINGOUIN:
        suggested = (
            "Three independent evaluators with expertise in LLM evaluation methodology "
            f"scored each of the {results['n_benchmarks']} benchmarks against the seven BQAI "
            "dimensions under a blinded protocol (no inter-evaluator communication prior to "
            "submission). Average inter-rater reliability across dimensions was "
            f"**ICC(2,k) = {np.mean(valid_iccs):.3f}** "
            f"(range {min(valid_iccs):.3f}–{max(valid_iccs):.3f}, "
            f"{interpret_icc(np.mean(valid_iccs))} agreement), and "
            f"**quadratic-weighted Cohen's κ = {np.mean(valid_kappas):.3f}** "
            f"({interpret_kappa(np.mean(valid_kappas))} agreement). Disagreements were "
            "resolved through consensus discussion with reference to the rubric evidence "
            "thresholds; final BQAI scores reflect post-reconciliation values. "
            "Pre-reconciliation raw scores, reconciliation logs, and analysis code are "
            "released in the supplementary repository."
        )
        add(f"> {suggested}")
    else:
        add("> [Insufficient data to auto-generate suggested text.]")

    return "\n".join(lines)


def print_console_report(results: dict) -> None:
    """Print a compact console summary."""
    print("=" * 72)
    print("BQAI INTER-RATER RELIABILITY ANALYSIS")
    print("=" * 72)
    print(f"Evaluators: {len(results['evaluators'])} ({', '.join(results['evaluators'])})")
    print(f"Benchmarks: {results['n_benchmarks']}")
    print()
    print(f"{'Q':<4}{'ICC(2,k)':>10}  {'95% CI':<16}{'Wt κ':>8}  {'mean|Δ|':>10}")
    print("-" * 60)
    for q in DIMENSIONS:
        d = results["per_dimension"][q]
        icc = d["icc"].get("ICC2k")
        ci = d["icc"].get("ICC2k_CI")
        kappa = d["weighted_kappa"]["avg_weighted_kappa"]
        mad = d["mean_abs_diff"]
        icc_str = f"{icc:.3f}" if icc is not None else "n/a"
        ci_str = f"[{ci[0]:.2f},{ci[1]:.2f}]" if ci else "n/a"
        k_str = f"{kappa:.3f}" if kappa is not None else "n/a"
        print(f"{q:<4}{icc_str:>10}  {ci_str:<16}{k_str:>8}  {mad:>10.3f}")
    print()


# ============================================================
# Main
# ============================================================
def main() -> None:
    parser = argparse.ArgumentParser(description="Compute BQAI inter-rater reliability")
    parser.add_argument(
        "--input-dir", type=Path,
        default=Path(__file__).parent.parent / "02_scoring" / "raw_scores",
        help="Directory containing BQAI_scoring_*.xlsx files (default: 02_scoring/raw_scores/)"
    )
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path(__file__).parent,
        help="Where to write iaa_results.json and iaa_report.md (default: 03_iaa/)"
    )
    parser.add_argument(
        "--write-reconciled", action="store_true",
        help="Also write reconciled_scores.csv (mean across evaluators). "
             "Off by default to avoid overwriting hand-reconciled scores."
    )
    args = parser.parse_args()

    if not HAS_PINGOUIN:
        print("[warning] pingouin not installed — ICC will use manual fallback (no CI).")
        print("          Install with: pip install pingouin\n")

    long_df = build_long_table(args.input_dir)

    results = {
        "evaluators": sorted(long_df["evaluator"].unique().tolist()),
        "n_benchmarks": int(long_df["benchmark"].nunique()),
        "per_dimension": {},
    }

    for q in DIMENSIONS:
        results["per_dimension"][q] = {
            "icc": compute_icc(long_df, q),
            "weighted_kappa": cohen_kappa_weighted(long_df, q),
            "pairwise_correlations": pairwise_correlations(long_df, q),
            "mean_abs_diff": mean_abs_diff(long_df, q),
        }

    # Console output
    print_console_report(results)

    # Reconciled scores (mean across evaluators) — only if explicitly requested
    if args.write_reconciled:
        reconciled = reconcile_mean(long_df)
        reconciled_path = args.input_dir.parent / "reconciled_scores.csv"
        reconciled.to_csv(reconciled_path, index=False, float_format="%.4f")
        print(f"Reconciled scores: {reconciled_path}")
    else:
        print("Reconciled scores: skipped (use --write-reconciled to enable).")

    # JSON output
    json_path = args.output_dir / "iaa_results.json"
    json_path.write_text(json.dumps(results, indent=2, default=str))
    print(f"JSON results:      {json_path}")

    # Markdown report
    md_path = args.output_dir / "iaa_report.md"
    md_path.write_text(build_text_report(results, long_df), encoding='utf-8')
    print(f"Markdown report:   {md_path}")


if __name__ == "__main__":
    main()
