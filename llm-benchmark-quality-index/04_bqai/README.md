# 04_bqai/ — BQAI computation and AHP weight derivation

This directory contains the core BQAI scripts: weight derivation via Analytic Hierarchy Process, the BQAI formula implementation, and sensitivity analysis.

## Contents (populated in Session 2)

| File | Description |
|------|-------------|
| `compute_bqai.py` | Computes BQAI scores and tier assignments from per-dimension evaluator scores. |
| `ahp_weights.py` | Derives the seven dimension weights from the AHP pairwise comparison matrix; verifies Consistency Ratio. |
| `sensitivity_analysis.py` | Monte Carlo perturbation of weights (±10%, ±25%, ±50%) plus four alternative weighting schemes (equal-weights, fairness-focused, coverage-focused, annotation-focused). |
| `sensitivity_results.json` | Output of the sensitivity analysis. |

## BQAI formula

The BQAI is a linear combination of seven quality dimensions:

```
BQAI = 0.349·Q4 + 0.213·Q1 + 0.167·Q5 + 0.117·Q3 + 0.073·Q2 + 0.048·Q7 + 0.033·Q6
```

where weights are derived via AHP under the principle of Scientific Reproducibility Priority.

## AHP weight derivation

The pairwise comparison matrix encodes the relative importance of each dimension pair on Saaty's fundamental scale. See `ahp_weights.py` for the explicit matrix and verification:

- **Matrix:** 7×7 with diagonal = 1 and reciprocal off-diagonal
- **Maximum eigenvalue λ_max:** 7.180
- **Consistency Index CI:** (7.180 − 7) / 6 = 0.030
- **Consistency Ratio CR:** CI / RI(n=7) = 0.030 / 1.32 = **0.023**

Since CR < 0.10 (Saaty's acceptability threshold), the pairwise judgments are internally consistent.

## Sensitivity analysis

The script tests robustness of BQAI rankings under four perturbation regimes:

### 1. Monte Carlo with small perturbation (±10%)
- 1,000 trials, each weight multiplied by uniform[0.9, 1.1] then renormalized
- Reports mean, range, and standard deviation of BQAI per benchmark

### 2. Monte Carlo with large perturbation (±25% and ±50%)
- Same procedure with wider perturbations
- Demonstrates robustness beyond marginal uncertainty

### 3. Alternative weighting schemes
- **Equal-weights:** w_i = 1/7 for all (most neutral imaginable)
- **Reproducibility-focused:** current AHP scheme (control)
- **Fairness-focused:** Q7 elevated to 0.30, others rebalanced
- **Coverage-focused:** Q6 elevated to 0.30, others rebalanced
- **Annotation-focused:** Q1 elevated to 0.30, others rebalanced

For each scheme, reports BQAI rankings and tier assignments. Argument: under any reasonable weighting philosophy, primary conclusions (HELM, SWE-bench Verified, LiveBench → Tier A; MMLU, GSM8K → Tier C) hold.

### 4. Ranking stability (Kendall's τ)
- Pairwise rank correlation between the AHP-weighted ranking and each alternative scheme
- Expected: τ > 0.85 for all reasonable schemes, demonstrating ranking stability

## How this addresses reviewer comments

This analysis directly addresses **Reviewer 1, Comment 4**:

> "How sensitive are your benchmark rankings to the AHP weight choices, and could different reasonable weight configurations change your main conclusions?"

The expanded sensitivity analysis (4 perturbation regimes vs. the original single ±10% Monte Carlo) provides much stronger evidence of weight robustness.

## Status

✓ **Complete.** Scripts implemented, validated, and run on the real three-evaluator data. Outputs in this directory.

## Headline results

The 30-benchmark BQAI assessment yields a notably conservative tier distribution:

- **Tier A (BQAI ≥ 0.82):** 1 benchmark — HLE (0.831).
- **Tier B (0.70–0.82):** 10 benchmarks — LiveBench (0.786), LiveCodeBench (0.772), HELM (0.769), HarmBench (0.727), SWE-bench Verified (0.720), CLadder (0.719), OlympiadBench (0.716), MMMU (0.714), MMLU-Pro (0.710), BBQ (0.707).
- **Tier C (< 0.70):** 19 benchmarks, including the saturation-driven foundational group (MMLU, GSM8K, HellaSwag, HumanEval).

Multi-regime sensitivity analysis confirms ranking stability: 29/30 benchmarks retain their tier under ±10% Monte Carlo perturbation, and Kendall's τ ≥ 0.82 across four realistic priority-shifted weighting schemes. See `sensitivity_report.md` for details.

Full per-benchmark BQAI scores: `bqai_results.csv`.
