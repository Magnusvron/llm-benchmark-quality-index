# 03_iaa/ — Inter-rater reliability analysis

This directory contains the formal psychometric validation of the BQAI scoring process: how much do independent evaluators agree, and is that agreement strong enough to support the framework's conclusions?

## Contents (populated by `compute_iaa.py`)

| File | Description |
|------|-------------|
| `compute_iaa.py` | Script that reads the three evaluator Excel files and produces all IAA metrics. |
| `iaa_results.json` | Machine-readable IAA output: ICC, weighted Cohen's κ, pairwise correlations, per-dimension breakdown. |
| `iaa_report.md` | Human-readable interpretation with suggested manuscript paragraph. |

## Metrics computed

For each of the seven quality dimensions (Q1–Q7), `compute_iaa.py` reports:

1. **Intraclass Correlation Coefficient ICC(2,k)** — appropriate for continuous scores from k random raters with absolute-agreement model. 95% confidence intervals included.
2. **ICC(2,1)** — single-rater reliability (more conservative than ICC(2,k)).
3. **Quadratic-weighted Cohen's κ** — computed pairwise between raters after binning scores into the four tiers (Low/Moderate/High/Excellent). Reports both per-pair and average.
4. **Pearson and Spearman correlations** — between all rater pairs, for continuous-score agreement assessment.
5. **Mean absolute difference** — between rater pairs, for backward-compatibility with the original (paper's reported 0.07).

## Interpretation thresholds

| Metric | Poor | Moderate | Good | Excellent |
|--------|------|----------|------|-----------|
| ICC(2,k) | <0.50 | 0.50–0.74 | 0.75–0.90 | >0.90 |
| Weighted κ | <0.40 | 0.40–0.59 | 0.60–0.79 | ≥0.80 |

## How this addresses reviewer comments

This analysis directly addresses **Reviewer 1, Comments 1 and 2**:

> "How do you ensure that the BQAI scoring (Q1–Q7) is objective and reproducible, given that it relies on expert judgment?"
> "Did you evaluate inter-annotator agreement for BQAI scoring? If not, how can the consistency and reliability of the scores be validated?"

Our response:
1. **Three independent evaluators** under a blinded protocol (not two as in original).
2. **Standard IAA metrics** (ICC + weighted κ) replace the prior single mean-absolute-difference measure.
3. **Operational rubric** with verifiable indicators (see `../01_rubric/`) minimizes subjective judgment.
4. **Full data and code released** in this repository allow any researcher to verify the analysis.

## Running the analysis

```bash
# Place filled Excel files in ../02_scoring/raw_scores/
python compute_iaa.py
```

Outputs:
- Console summary table with all IAA metrics
- `iaa_results.json` machine-readable
- `iaa_report.md` human-readable

## Status

✓ **Complete.** All three evaluators submitted; IAA computed; outputs in `iaa_results.json` and `iaa_report.md`.

## Headline results

Mean ICC(2,k) = **0.855** across the seven dimensions (range 0.744–0.943), indicating **good agreement** under standard psychometric thresholds. Mean quadratic-weighted Cohen's κ = **0.541** (moderate agreement under the more conservative ordinal interpretation).

| Dim | ICC(2,k) | 95% CI | Weighted κ | Mean \|Δ\| |
|-----|----------|--------|------------|-----------|
| Q1 Annotation | 0.744 | [0.54, 0.87] | 0.383 | 0.060 |
| Q2 Clarity | 0.802 | [0.64, 0.90] | 0.461 | 0.046 |
| Q3 Standardization | 0.828 | [0.69, 0.91] | 0.580 | 0.060 |
| Q4 Reproducibility | 0.884 | [0.79, 0.94] | 0.543 | 0.064 |
| Q5 Robustness | 0.852 | [0.65, 0.93] | 0.645 | 0.162 |
| Q6 Coverage | 0.928 | [0.86, 0.96] | 0.671 | 0.087 |
| Q7 Fairness | 0.943 | [0.89, 0.97] | 0.502 | 0.064 |

Q5 (robustness/contamination) exhibited the largest disagreement (mean |Δ| = 0.162), reflecting genuine conceptual variation among evaluators about how to penalize benchmark saturation. We retain this disagreement transparently in the aggregated scores. Full discussion in [`iaa_report.md`](iaa_report.md).
