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

🟡 **Pending evaluator submissions** — the `compute_iaa.py` script is implemented in `../04_bqai/` (will be moved here in Session 2) and ready to run; results will be added after the three evaluators submit.
