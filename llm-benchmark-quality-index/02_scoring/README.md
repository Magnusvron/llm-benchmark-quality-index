# 02_scoring/ — Raw evaluator scores

This directory contains the scoring data from three independent evaluators who scored the 30 BQAI sample benchmarks across the seven quality dimensions.

## Contents

| File | Description |
|------|-------------|
| `raw_scores/BQAI_scoring_GomezOlvera.xlsx` | Evaluator 1's filled scoring sheet (30 benchmarks × 7 dimensions). |
| `raw_scores/BQAI_scoring_Miranda.xlsx`     | Evaluator 2's filled scoring sheet. |
| `raw_scores/BQAI_scoring_Terven.xlsx`      | Evaluator 3's filled scoring sheet. |
| `reconciled_scores.csv` | Aggregated scores: unweighted mean across the three evaluators per (benchmark, dimension). Input to `04_bqai/compute_bqai.py`. |

## Protocol summary

Three independent evaluators with documented expertise in LLM evaluation methodology scored each benchmark under a **blinded protocol**: each evaluator worked from the same operational rubric (`../01_rubric/BQAI_rubric_full.md`) and the same Excel template (`../docs/BQAI_scoring_template_ES.xlsx`), with no inter-evaluator communication during the scoring phase. Each scored every benchmark on every dimension Q1–Q7 in `[0, 1]`.

After all three submitted their scoring sheets, the raw per-evaluator scores were used to compute formal inter-rater reliability metrics (see `../03_iaa/`). Final BQAI scores in `reconciled_scores.csv` are the **unweighted mean** of the three evaluator scores per cell.

## Aggregation choice

We use unweighted mean aggregation rather than post-hoc consensus reconciliation. This choice preserves each evaluator's independent judgment in the aggregated score and yields IAA metrics (ICC, weighted κ) that reflect genuine pre-aggregation agreement rather than agreement engineered through reconciliation discussion. Sources of disagreement, particularly in Q5 (robustness/contamination, where mean |Δ| = 0.162), are documented transparently in `../03_iaa/iaa_report.md` rather than resolved.

This is an intentional methodological choice: we report the BQAI as it emerges from independent blinded scoring, including its uncertainty, rather than presenting a more confident-looking consensus that would mask the genuine epistemic variation among expert evaluators.

## Evaluators

The three evaluators are co-authors of the accompanying paper. Their backgrounds span:
- Multimodal vision-language model research and benchmark methodology (CICATA-Querétaro, Instituto Politécnico Nacional).
- LLM evaluation infrastructure and applied NLP research (Universidad Autónoma de Querétaro).
- LLM benchmark design and computer vision evaluation (CICATA-Querétaro, Instituto Politécnico Nacional).

Filenames identify evaluators directly because they are public co-authors; raw scores are openly released for independent verification of the IAA analysis.

## Regenerating `reconciled_scores.csv`

```bash
python ../03_iaa/compute_iaa.py --write-reconciled
```

This reads all `raw_scores/BQAI_scoring_*.xlsx` files in this directory, computes IAA, and writes the aggregated mean scores to `reconciled_scores.csv`.
