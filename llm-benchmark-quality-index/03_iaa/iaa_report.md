# BQAI Inter-Rater Reliability Report

**Evaluators (n=3):** GomezOlvera, Miranda, Terven
**Benchmarks scored:** 30
**Dimensions:** Q1, Q2, Q3, Q4, Q5, Q6, Q7

## Per-dimension IAA metrics

| Dim | ICC(2,k) | 95% CI | Interpretation | Weighted κ | Interpretation | Mean \|Δ\| |
|-----|----------|--------|----------------|------------|----------------|-----------|
| Q1 | 0.744 | [0.54, 0.87] | moderate | 0.383 | weak | 0.060 |
| Q2 | 0.802 | [0.64, 0.90] | good | 0.461 | moderate | 0.046 |
| Q3 | 0.828 | [0.69, 0.91] | good | 0.580 | moderate | 0.060 |
| Q4 | 0.884 | [0.79, 0.94] | good | 0.543 | moderate | 0.064 |
| Q5 | 0.852 | [0.65, 0.93] | good | 0.645 | substantial | 0.162 |
| Q6 | 0.928 | [0.86, 0.96] | excellent | 0.671 | substantial | 0.087 |
| Q7 | 0.943 | [0.89, 0.97] | excellent | 0.502 | moderate | 0.064 |

## Aggregate metrics

- **Mean ICC(2,k):** 0.855 (range 0.744 – 0.943) → **good** agreement
- **Mean weighted κ:** 0.541 (range 0.383 – 0.671) → **moderate** agreement

## Interpretation guide

| Metric | Poor | Moderate | Good/Substantial | Excellent/Strong |
|--------|------|----------|------------------|------------------|
| ICC(2,k) | <0.50 | 0.50–0.74 | 0.75–0.90 | >0.90 |
| Weighted κ | <0.40 | 0.40–0.59 | 0.60–0.79 | ≥0.80 |

## Suggested manuscript text (§7.1)

> Three independent evaluators with expertise in LLM evaluation methodology scored each of the 30 benchmarks against the seven BQAI dimensions under a blinded protocol (no inter-evaluator communication prior to submission). Average inter-rater reliability across dimensions was **ICC(2,k) = 0.855** (range 0.744–0.943, good agreement), and **quadratic-weighted Cohen's κ = 0.541** (moderate agreement). Disagreements were resolved through consensus discussion with reference to the rubric evidence thresholds; final BQAI scores reflect post-reconciliation values. Pre-reconciliation raw scores, reconciliation logs, and analysis code are released in the supplementary repository.