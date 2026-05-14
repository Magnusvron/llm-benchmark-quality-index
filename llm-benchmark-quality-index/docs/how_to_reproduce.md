# How to reproduce the BQAI analysis

This guide walks through every step required to reproduce the BQAI results reported in the paper, starting from a clean environment.

## Prerequisites

- **Python 3.10 or newer**
- **Git**
- ~500 MB free disk space
- Internet access for benchmark documentation lookups (if you re-score)

## Step 1: Clone the repository

```bash
git clone https://github.com/Magnusvron/llm-benchmark-quality-index.git
cd llm-benchmark-quality-index
```

## Step 2: Set up the Python environment

We recommend a virtual environment to isolate dependencies:

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

The full dependency list is small (pandas, numpy, scipy, pingouin, scikit-learn, openpyxl, matplotlib).

## Step 3: Verify the corpus and sample

```bash
# Sanity-check the corpus and sample CSVs
python -c "
import pandas as pd
corpus = pd.read_csv('06_corpus/benchmarks_63.csv')
sample = pd.read_csv('06_corpus/benchmarks_sample_30.csv')
print(f'Corpus: {len(corpus)} benchmarks')
print(f'Sample: {len(sample)} benchmarks ({len(sample)/len(corpus)*100:.0f}% coverage)')
print(f'Sample by dimension:')
print(sample.groupby('primary_dimension').size())
"
```

Expected output:
```
Corpus: 63 benchmarks
Sample: 30 benchmarks (48% coverage)
```

## Step 4: Verify the AHP weights (Session 2 deliverable)

```bash
python 04_bqai/ahp_weights.py
```

This script:
1. Loads the 7×7 pairwise comparison matrix.
2. Computes the principal eigenvector (= dimension weights).
3. Computes the Consistency Ratio (CR).
4. Confirms CR < 0.10 (Saaty's acceptability threshold).
5. Prints the weights.

Expected output:
```
Weights derived via AHP:
  Q4 (Reproducibility):   0.349
  Q1 (Annotation):        0.213
  Q5 (Robustness):        0.167
  Q3 (Standardization):   0.117
  Q2 (Clarity):           0.073
  Q7 (Fairness):          0.048
  Q6 (Coverage):          0.033

λ_max = 7.180
CI = 0.030
CR = 0.023  ✓ (< 0.10, judgments consistent)
```

## Step 5: Compute inter-rater reliability (after evaluator data is in place)

If the raw evaluator scores are present in `02_scoring/raw_scores/`:

```bash
python 03_iaa/compute_iaa.py
```

This produces `03_iaa/iaa_results.json` and `03_iaa/iaa_report.md`.

To also generate `02_scoring/reconciled_scores.csv` as the mean across evaluators
(overwriting any existing file):

```bash
python 03_iaa/compute_iaa.py --write-reconciled
```

If you want to re-run the scoring exercise with new evaluators:
1. Share `BQAI_Protocolo_ES.docx` and `BQAI_scoring_template_ES.xlsx` (in `docs/`) with three independent evaluators.
2. Wait for filled Excel files back.
3. Place them in `02_scoring/raw_scores/`.
4. Run `python 03_iaa/compute_iaa.py --write-reconciled`.

## Step 6: Compute BQAI scores

```bash
python 04_bqai/compute_bqai.py
```

Reads `02_scoring/reconciled_scores.csv` (the post-consensus scores) and produces final BQAI scores with tier assignments.

## Step 7: Run sensitivity analysis

```bash
python 04_bqai/sensitivity_analysis.py
```

Tests robustness under:
- Monte Carlo perturbation (±10%, ±25%, ±50%)
- Four alternative weighting schemes (equal-weights, fairness-focused, coverage-focused, annotation-focused)
- Kendall's τ ranking stability

Outputs `04_bqai/sensitivity_results.json`.

## Step 8: Regenerate figures (optional)

```bash
python 07_figures/generate_figures.py
```

Produces all figures from data files. Outputs PDF and PNG; not committed to git (regenerable).

## Verifying you reproduced correctly

The repository ships with reference outputs in each subdirectory. After running each step, compare your output to:
- `03_iaa/iaa_results.json` (reference)
- `04_bqai/sensitivity_results.json` (reference)
- `02_scoring/reconciled_scores.csv` (reference)

Numerical results should match to ±0.001 (small rounding differences are normal).

## Troubleshooting

**`pingouin` installation fails:**
Sometimes pingouin has heavy dependencies. Try installing without it; the script falls back to manual ICC computation:
```bash
pip install -r requirements.txt --ignore-installed pingouin
```

**Excel reading errors:**
If evaluator files were saved by old Excel versions, openpyxl may complain. Re-save the file in modern .xlsx format and retry.

**Different platform, slightly different results:**
Random seeds are fixed in the scripts; you should get bit-identical results. If you don't, file an issue with your Python and numpy versions.

## Getting help

- **Methodology questions:** open a GitHub issue with the `methodology` label.
- **Reproduction issues:** open a GitHub issue with the `reproducibility` label, including your platform, Python version, and the exact error.
- **Direct contact:** `ruben.cicata@gmail.com`
