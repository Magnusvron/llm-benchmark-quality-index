# 02_scoring/raw_scores/ — Filled scoring sheets

Three Excel files, one per independent blinded evaluator, each containing scores for the 30 BQAI sample benchmarks across the seven quality dimensions Q1–Q7.

## Files

| File | Evaluator | Scoring date |
|------|-----------|--------------|
| `BQAI_scoring_GomezOlvera.xlsx` | Rubén Gómez Olvera (CICATA-Querétaro, IPN) | 2026-05-13 |
| `BQAI_scoring_Miranda.xlsx`     | Carlos E. Miranda (UAQ)                   | 2026-12-05 |
| `BQAI_scoring_Terven.xlsx`      | Juan Terven (CICATA-Querétaro, IPN)       | 2026-05-12 |

## Format

Each file is a copy of the master template (`../../docs/BQAI_scoring_template_ES.xlsx`) with the evaluator's scores filled in. Sheets:

- `Instrucciones`: Spanish-language summary of the protocol.
- `Rúbrica`: Operational scoring rubric (same as `../../01_rubric/BQAI_rubric_full.md`).
- `Scoring`: The filled data. Header row at row 6; benchmark rows from row 7 onward, with columns B (benchmark name), C (primary dimension), F–L ($Q_1$–$Q_7$), and N (optional notes).

## How these were collected

Each evaluator received the master template and the protocol document (`../../docs/BQAI_Protocolo_ES.docx`) by email, with explicit instructions not to discuss scores with other evaluators until all three sheets had been submitted. Each independently filled the 30×7 cells based on their reading of primary sources (benchmark papers, repositories, leaderboards) and the operational rubric.

These files are the **pre-aggregation** raw data. To regenerate the aggregated scores and IAA metrics from them, run `../../03_iaa/compute_iaa.py`.
