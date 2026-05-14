# 06_corpus/ — Benchmark corpus and sample selection

This directory documents the 63-benchmark corpus curated in the paper, the 30-benchmark subsample selected for BQAI scoring, the operational criteria that drove selection, and a quantitative representativeness analysis.

## Contents

| File | Purpose |
|------|---------|
| `benchmarks_63.csv` | Full corpus: name, dimension, subcategory, track, year, citation key, URL, and whether included in BQAI sample. |
| `benchmarks_sample_30.csv` | BQAI sample with per-benchmark selection rationale (which criterion C1–C5 motivated inclusion). |
| `selection_criteria.md` | Documentation of the five selection criteria (C1–C5) with justification and the distribution table. |
| `representativeness_analysis.md` | Quantitative comparison between corpus and sample across nine structural properties. |

## How this addresses reviewer comments

This documentation specifically responds to **Reviewer 2, Comment 1**:

> "the paper applies the full BQAI assessment to a subset of 21 benchmarks, while the broader corpus contains 63 benchmarks. ... the sampling logic should be made much more explicit. The reader needs to understand why these 21 benchmarks were selected, whether they are representative of the full corpus, and how sensitive the conclusions are to this selection."

Our response:
1. We expanded the sample from 21 to **30 benchmarks** (48% of corpus).
2. We defined **five explicit selection criteria** (C1–C5) that any independent researcher could apply.
3. We provide **per-benchmark justification** documenting which criteria motivated each inclusion.
4. We conduct a **representativeness analysis** demonstrating that the sample preserves the corpus's key structural properties.

## Key statistics

- **Corpus size:** 63 benchmarks across 6 dimensions, 20 subcategories, 2012–2025.
- **Sample size:** 30 benchmarks (48% of corpus, 70% of subcategories).
- **Minimum benchmarks per dimension:** 4 (was 2 in original 21-benchmark sample).
- **Track ratio in sample:** 20 Core / 10 Emerging.

For per-dimension breakdowns and full justification, see `selection_criteria.md` and `representativeness_analysis.md`.
