# 02_scoring/ — Raw evaluator scores

This directory contains the **pre-reconciliation** scoring data from three independent evaluators who scored the 30 BQAI sample benchmarks across the seven quality dimensions.

## Contents (populated after evaluator submissions)

| File | Description |
|------|-------------|
| `raw_scores/evaluator_1.csv` | Evaluator 1's independent scores, 30 benchmarks × 7 dimensions. |
| `raw_scores/evaluator_2.csv` | Evaluator 2's independent scores. |
| `raw_scores/evaluator_3.csv` | Evaluator 3's independent scores. |
| `reconciled_scores.csv` | Final scores after consensus reconciliation. |
| `reconciliation_log.md` | Decisions made during reconciliation, with evidence cited per dimension. |
| `evaluator_profiles.md` | Background of each evaluator (anonymized): expertise, role, affiliation type. |

## Protocol summary

Three evaluators with expertise in LLM evaluation methodology scored each benchmark **independently and blindly** (no communication during scoring). The protocol is documented in `BQAI_Protocolo_ES.docx` (sent to evaluators separately).

After all three submitted their scores, the raw scores were used to compute inter-rater reliability metrics (see `../03_iaa/`). Disagreements with absolute difference > 0.20 on any dimension were resolved through structured consensus discussion with reference to the operational rubric. The reconciliation log records each consensus decision.

## Privacy and anonymization

The `raw_scores/` files contain scoring data only; no personally identifying information beyond a numeric evaluator ID. Evaluator profiles in `evaluator_profiles.md` describe expertise type (e.g., "PhD in NLP", "MS student researcher", "industry practitioner") without identifying individuals.

## Status

🟡 **Pending evaluator submissions** — placeholder structure in place; real data will be added after the three evaluators return their scored Excel templates.
