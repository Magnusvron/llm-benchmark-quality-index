"""
AHP Weight Derivation for BQAI
================================

Derives the seven BQAI dimension weights from the pairwise comparison matrix
using the Analytic Hierarchy Process (Saaty, 1980).

The matrix encodes the principle of Scientific Reproducibility Priority:
- Q4 (Reproducibility) is weighted most heavily because irreproducible
  benchmarks cannot support cumulative scientific progress.
- Q1 (Annotation Quality) and Q5 (Robustness) follow as second-order
  priorities essential for frontier evaluation validity.
- Q6 (Coverage) and Q7 (Fairness) receive lower weights — they matter
  but do not invalidate a benchmark on their own.

Usage:
    python ahp_weights.py [--export weights.json]

Outputs:
    - Console table with derived weights
    - Verification that Consistency Ratio (CR) < 0.10
    - Optional JSON export of weights for use by other scripts
"""

import argparse
import json
from pathlib import Path

import numpy as np


# ============================================================
# AHP Pairwise Comparison Matrix
# ============================================================
# Matrix element a[i][j] = importance of dimension i over dimension j
# on Saaty's fundamental scale:
#   1   = equal importance
#   3   = moderately more important
#   5   = strongly more important
#   7   = very strongly more important
#   9   = extremely more important
#   1/3 = moderately less important
#   1/5 = strongly less important
#   etc.
#
# Reciprocal property: a[i][j] = 1 / a[j][i]
# Diagonal: a[i][i] = 1
#
# This matrix is reproduced from Table 8 of the paper.

DIMENSIONS = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"]

DIMENSION_NAMES = {
    "Q1": "Annotation Quality and Consistency",
    "Q2": "Instructional Clarity and Format",
    "Q3": "Standardization and Versioning",
    "Q4": "Reproducibility and Baselines",
    "Q5": "Robustness and Contamination Resistance",
    "Q6": "Cognitive Skill Coverage",
    "Q7": "Bias Mitigation and Cross-Cultural Validity",
}

# Pairwise comparison matrix (paper Table 8)
PAIRWISE_MATRIX = np.array([
    # Q1     Q2    Q3    Q4    Q5    Q6   Q7
    [1,      3,    2,    1/2,  2,    5,   4   ],  # Q1: Annotation
    [1/3,    1,    1/2,  1/5,  1/3,  3,   2   ],  # Q2: Clarity
    [1/2,    2,    1,    1/3,  1/2,  4,   3   ],  # Q3: Standardization
    [2,      5,    3,    1,    3,    7,   6   ],  # Q4: Reproducibility
    [1/2,    3,    2,    1/3,  1,    5,   4   ],  # Q5: Robustness
    [1/5,    1/3,  1/4,  1/7,  1/5,  1,   1/2 ],  # Q6: Coverage
    [1/4,    1/2,  1/3,  1/6,  1/4,  2,   1   ],  # Q7: Fairness
])

# Random Index values (Saaty 1980, standard reference)
# Used to compute Consistency Ratio: CR = CI / RI(n)
RANDOM_INDEX = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
}


def verify_matrix_structure(matrix: np.ndarray) -> None:
    """Sanity-check that the pairwise matrix is well-formed."""
    n = matrix.shape[0]
    assert matrix.shape == (n, n), f"Matrix must be square, got {matrix.shape}"
    assert n == len(DIMENSIONS), f"Matrix size {n} != #dimensions {len(DIMENSIONS)}"

    # Diagonal must be 1
    for i in range(n):
        assert abs(matrix[i, i] - 1) < 1e-9, f"Diagonal [{i},{i}] != 1"

    # Reciprocal property: a[i][j] * a[j][i] == 1
    for i in range(n):
        for j in range(n):
            product = matrix[i, j] * matrix[j, i]
            assert abs(product - 1) < 1e-9, (
                f"Reciprocal violated at [{i},{j}]: "
                f"{matrix[i,j]} * {matrix[j,i]} = {product}"
            )


def compute_weights(matrix: np.ndarray) -> tuple[np.ndarray, float]:
    """Compute priority weights as the normalized principal eigenvector.

    Returns:
        weights: array of length n, summing to 1.0
        lambda_max: the principal (largest) eigenvalue, used for CR
    """
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    # Principal eigenvalue is the largest real one
    real_eigenvalues = eigenvalues.real
    max_idx = np.argmax(real_eigenvalues)
    lambda_max = float(real_eigenvalues[max_idx])

    # Principal eigenvector (real part)
    principal = eigenvectors[:, max_idx].real
    # Normalize to sum to 1
    weights = principal / principal.sum()
    # Ensure positive (eigenvectors can come out negated)
    if weights[0] < 0:
        weights = -weights

    return weights, lambda_max


def consistency_ratio(lambda_max: float, n: int) -> tuple[float, float, float]:
    """Compute Consistency Index (CI) and Consistency Ratio (CR).

    CI = (lambda_max - n) / (n - 1)
    CR = CI / RI(n)

    A matrix is considered consistent if CR < 0.10.
    """
    ci = (lambda_max - n) / (n - 1)
    ri = RANDOM_INDEX[n]
    cr = ci / ri if ri > 0 else 0.0
    return ci, ri, cr


def print_report(weights: np.ndarray, lambda_max: float,
                 ci: float, ri: float, cr: float) -> None:
    """Print human-readable verification report."""
    n = len(weights)
    print("=" * 72)
    print("AHP WEIGHT DERIVATION FOR BQAI")
    print("=" * 72)
    print()
    print("Pairwise comparison matrix (7×7):")
    print(_format_matrix(PAIRWISE_MATRIX))
    print()
    print("-" * 72)
    print("Derived weights (normalized principal eigenvector):")
    print("-" * 72)
    print(f"  {'ID':<4} {'Dimension':<46} {'Weight':>10}")
    # Sort by weight descending for readability
    order = np.argsort(-weights)
    for idx in order:
        dim_id = DIMENSIONS[idx]
        dim_name = DIMENSION_NAMES[dim_id]
        w = weights[idx]
        marker = "  ⭐" if w == weights.max() else ""
        print(f"  {dim_id:<4} {dim_name:<46} {w:>10.4f}{marker}")
    print(f"  {'':<4} {'(sum)':<46} {weights.sum():>10.4f}")
    print()
    print("-" * 72)
    print("Consistency verification:")
    print("-" * 72)
    print(f"  λ_max (principal eigenvalue) : {lambda_max:.4f}")
    print(f"  n  (matrix dimension)        : {n}")
    print(f"  CI = (λ_max - n) / (n - 1)   : {ci:.4f}")
    print(f"  RI (random index for n={n})   : {ri:.4f}")
    print(f"  CR = CI / RI                  : {cr:.4f}")
    print()
    status = "✓ PASS" if cr < 0.10 else "✗ FAIL"
    print(f"  Threshold: CR < 0.10 → {status}")
    if cr < 0.10:
        print("  Judgments are internally consistent. Weights are valid.")
    else:
        print("  Judgments are NOT internally consistent. Revise matrix.")
    print()


def _format_matrix(m: np.ndarray) -> str:
    """Pretty-print the pairwise matrix with fractions for small values."""
    n = m.shape[0]
    rows = []
    # Header
    header = "      " + "  ".join(f"{d:>6}" for d in DIMENSIONS)
    rows.append(header)
    rows.append("    " + "-" * (8 * n))
    for i in range(n):
        cells = []
        for j in range(n):
            v = m[i, j]
            if v >= 1:
                cells.append(f"{v:>6.2f}")
            else:
                # Show as fraction for readability
                cells.append(f"{f'1/{1/v:.0f}':>6}")
        rows.append(f"  {DIMENSIONS[i]:<3} " + "  ".join(cells))
    return "\n".join(rows)


def export_weights(weights: np.ndarray, lambda_max: float,
                   ci: float, cr: float, path: Path) -> None:
    """Export weights to JSON for use by downstream scripts."""
    payload = {
        "weights": {DIMENSIONS[i]: float(weights[i]) for i in range(len(weights))},
        "dimension_names": DIMENSION_NAMES,
        "lambda_max": float(lambda_max),
        "consistency_index": float(ci),
        "consistency_ratio": float(cr),
        "consistent": bool(cr < 0.10),
        "derivation": "Analytic Hierarchy Process (Saaty, 1980)",
        "principle": "Scientific Reproducibility Priority",
    }
    path.write_text(json.dumps(payload, indent=2))
    print(f"Weights exported to: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--export", type=Path, default=None,
        help="Optional path to write weights as JSON (for compute_bqai.py)"
    )
    args = parser.parse_args()

    verify_matrix_structure(PAIRWISE_MATRIX)
    weights, lambda_max = compute_weights(PAIRWISE_MATRIX)
    ci, ri, cr = consistency_ratio(lambda_max, len(DIMENSIONS))

    print_report(weights, lambda_max, ci, ri, cr)

    if args.export:
        export_weights(weights, lambda_max, ci, cr, args.export)


if __name__ == "__main__":
    main()
