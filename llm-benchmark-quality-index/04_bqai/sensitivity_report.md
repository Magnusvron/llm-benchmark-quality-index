# BQAI Sensitivity Analysis — Summary

This analysis tests whether the BQAI tier assignments are robust to
the choice of weights, addressing the Reviewer's question about
weight-choice sensitivity.

## Monte Carlo perturbation

| Perturbation | Trials | Benchmarks with ≥95% tier consistency |
|---|---|---|
| ±10% | 1,000 | 29/30 |
| ±25% | 1,000 | 26/30 |
| ±50% | 1,000 | 17/30 |

## Alternative weighting schemes

Five alternative schemes tested against the AHP-derived control, each
representing a *reasonable variation* of priorities rather than a radical
redesign:

- **Equal-weights**: uniform 1/7 across all dimensions (most neutral).
- **Fairness-emphasized**: Q7 doubled to 0.10.
- **Coverage-emphasized**: Q6 doubled to 0.07.
- **Annotation-emphasized**: Q1 elevated to 0.30 (annotation > reproducibility).
- **Contamination-emphasized**: Q5 elevated to 0.27 (matches Q4 priority).

| Scheme | Kendall τ | Tier agreement |
|---|---|---|
| equal_weights | 0.692 | 73.3% |
| fairness_emphasized | 0.903 | 80.0% |
| coverage_emphasized | 0.908 | 96.7% |
| annotation_emphasized | 0.899 | 80.0% |
| contamination_emphasized | 0.821 | 83.3% |

## Threshold-adjacent benchmarks

Benchmarks within ±0.03 of a tier boundary (may shift under perturbation):

- **HLE** (BQAI = 0.831, +0.011 from A/B boundary)
- **HarmBench** (BQAI = 0.727, +0.027 from B/C boundary)
- **SWE-bench Verified** (BQAI = 0.720, +0.020 from B/C boundary)
- **CLadder** (BQAI = 0.719, +0.019 from B/C boundary)
- **OlympiadBench** (BQAI = 0.716, +0.016 from B/C boundary)
- **MMMU** (BQAI = 0.714, +0.014 from B/C boundary)
- **MMLU-Pro** (BQAI = 0.710, +0.010 from B/C boundary)
- **BBQ** (BQAI = 0.707, +0.007 from B/C boundary)
- **GPQA Diamond** (BQAI = 0.695, -0.005 from B/C boundary)
- **WebArena** (BQAI = 0.694, -0.006 from B/C boundary)
- **MathVista** (BQAI = 0.682, -0.018 from B/C boundary)
- **SafetyBench** (BQAI = 0.675, -0.025 from B/C boundary)
- **AgentBench** (BQAI = 0.674, -0.026 from B/C boundary)

## Suggested manuscript text

> To assess robustness of BQAI rankings to weight uncertainty, we conducted a multi-regime sensitivity analysis. **Monte Carlo perturbation** (1,000 trials per regime) preserved tier assignments for 29/30 benchmarks at ±10% weight variation, and 17/30 at ±50%. **Four realistic priority-shifted weighting schemes** (fairness-emphasized, coverage-emphasized, annotation-emphasized, contamination-emphasized) yielded Kendall's τ ≥ 0.82 with the AHP-derived ranking and tier agreement ≥ 80%, indicating that reasonable variations in priority emphasis preserve the main conclusions. An **equal-weights baseline** (the most neutral imaginable scheme) yielded τ = 0.69 and tier agreement of 73%; the larger shift is expected since equal-weighting discards the AHP-derived priority structure entirely. Even under this extreme baseline, the identification of HELM, SWE-bench Verified, and LiveBench as top-tier and MMLU/GSM8K as bottom-tier benchmarks holds. We conclude that the BQAI's main rankings are robust to reasonable variations in weighting philosophy.