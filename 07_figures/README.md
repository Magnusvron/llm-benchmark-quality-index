# 07_figures/ — Figure generation scripts

This directory contains scripts that regenerate the figures and tables in the paper from the underlying data files in this repository, ensuring full reproducibility.

## Contents (populated in Session 2)

| File | Description |
|------|-------------|
| `generate_figures.py` | Master script that produces all figures from data. |
| `figure_bqai_distribution.py` | Distribution of BQAI scores across the 30-benchmark sample. |
| `figure_tier_heatmap.py` | Heatmap of per-dimension scores for each benchmark, colored by tier. |
| `figure_sensitivity.py` | Visualization of Monte Carlo sensitivity results. |
| `figure_iaa_correlations.py` | Visualization of inter-rater agreement (correlations + ICC bars). |

## How to regenerate figures

```bash
pip install -r ../requirements.txt
python generate_figures.py
```

Outputs are PDF and PNG files (excluded from version control via `.gitignore` since they are regenerable from the data).

## Status

🟡 **Scripts to be implemented in Session 2.** Figure specifications drafted; implementation pending.
