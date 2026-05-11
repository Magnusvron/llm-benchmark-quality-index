# LLM Benchmark Quality Index (BQAI)

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Reproducibility](https://img.shields.io/badge/reproducibility-validated-brightgreen.svg)](docs/how_to_reproduce.md)

> Reproducibility package for the **Benchmark Quality Assurance Index (BQAI)**, a quantitative AHP-weighted framework for assessing the scientific quality of evaluation benchmarks used to measure Large Language Models.

This repository contains the full supplementary materials for:

> Gómez, R., Miranda, C. E., Romero-González, J.-A., Córdova-Esparza, D.-M., Alfonzo Francia, G., Chávez-Urbiola, E.-A., Ramirez-Pedraza, A., & Terven, J. (2026). *How to Measure the Intelligence of Large Language Models: An Analysis of Datasets, Benchmarks, and Metrics.*

---

## What is BQAI?

The **Benchmark Quality Assurance Index (BQAI)** is a composite metric that quantifies the intrinsic scientific quality of LLM evaluation benchmarks across seven dimensions:

| ID  | Dimension                                | Weight |
|-----|------------------------------------------|--------|
| Q1  | Annotation Quality and Consistency       | 0.213  |
| Q2  | Instructional Clarity and Format         | 0.073  |
| Q3  | Standardization and Versioning           | 0.117  |
| Q4  | Reproducibility and Baseline Implementations | **0.349** |
| Q5  | Robustness and Contamination Resistance  | 0.167  |
| Q6  | Cognitive Skill Coverage                 | 0.033  |
| Q7  | Bias Mitigation and Cross-Cultural Validity | 0.048  |

Weights are derived via the Analytic Hierarchy Process (AHP) under the principle of **Scientific Reproducibility Priority**, with documented Consistency Ratio of 0.023 (well below the 0.10 threshold).

Benchmarks are classified into three tiers:
- **Tier A (BQAI ≥ 0.82):** Gold standards suitable for primary frontier model evaluation.
- **Tier B (0.70 ≤ BQAI < 0.82):** Moderate quality, useful with acknowledged limitations.
- **Tier C (BQAI < 0.70):** Substantial methodological limitations; not recommended for primary claims.

---

## Repository structure

Each numbered directory corresponds to a distinct component of the BQAI framework:

```
llm-benchmark-quality-index/
├── 01_rubric/                  Operational scoring rubric for Q1-Q7
├── 02_scoring/                 Raw scores from 3 evaluators + reconciliation log
├── 03_iaa/                     Inter-rater reliability analysis (ICC, weighted κ)
├── 04_bqai/                    BQAI computation + AHP weight derivation + sensitivity
├── 05_performance_matrix/      Model × benchmark performance matrix with source traceability
├── 06_corpus/                  63-benchmark corpus + 30-benchmark BQAI sample with selection criteria
├── 07_figures/                 Figure generation scripts
├── data/                       Consolidated raw data
└── docs/                       Reproduction guide, FAQ, methodology notes
```

Each subdirectory contains its own README explaining its contents.

---

## Quick start

### Reproduce BQAI computation

```bash
git clone https://github.com/Magnusvron/llm-benchmark-quality-index.git
cd llm-benchmark-quality-index
pip install -r requirements.txt

# Compute BQAI scores from reconciled evaluator data
python 04_bqai/compute_bqai.py

# Verify AHP weight derivation and consistency ratio
python 04_bqai/ahp_weights.py

# Run sensitivity analysis (Monte Carlo + alternative weighting schemes)
python 04_bqai/sensitivity_analysis.py
```

### Compute inter-rater reliability

```bash
# After placing the three evaluator scoring sheets in 02_scoring/raw_scores/
python 03_iaa/compute_iaa.py
```

For a step-by-step reproduction guide, see [`docs/how_to_reproduce.md`](docs/how_to_reproduce.md).

---

## Key results

When applied to the 30-benchmark sample (representing 48% of the curated 63-benchmark corpus):

- **Tier A benchmarks** (gold standards): HELM, SWE-bench Verified, LiveBench, LiveCodeBench, TruthfulQA
- **Tier C benchmarks** (substantial limitations): GSM8K, MMLU
- **Sensitivity:** Tier classifications remain robust across Monte Carlo perturbation (±10% to ±50% weights) and four alternative weighting schemes (equal-weights, fairness-focused, coverage-focused, annotation-focused).
- **Inter-rater reliability:** ICC(2,k) and quadratic-weighted Cohen's κ reported in [`03_iaa/iaa_report.md`](03_iaa/iaa_report.md).

---

## Citation

If you use this framework or these materials, please cite both the paper and this repository:

```bibtex
@article{gomez2026bqai,
  title   = {How to Measure the Intelligence of Large Language Models:
             An Analysis of Datasets, Benchmarks, and Metrics},
  author  = {G{\'o}mez, Rub{\'e}n and Miranda, Carlos E. and
             Romero-Gonz{\'a}lez, Julio-Alejandro and
             C{\'o}rdova-Esparza, Diana-Margarita and
             Alfonzo Francia, Gendry and Ch{\'a}vez-Urbiola, Edgar-Arturo and
             Ramirez-Pedraza, Alfonso and Terven, Juan},
  year    = {2026},
  journal = {(under review)}
}

@software{gomez2026bqai_repo,
  author  = {G{\'o}mez, Rub{\'e}n and others},
  title   = {LLM Benchmark Quality Index: Reproducibility Package},
  year    = {2026},
  url     = {https://github.com/Magnusvron/llm-benchmark-quality-index},
  version = {1.0.0}
}
```

Machine-readable citation metadata is in [`CITATION.cff`](CITATION.cff).

---

## Licensing

- **Code** (`*.py`, `*.js`, scripts): MIT License — see [`LICENSE`](LICENSE).
- **Data, rubric, and documentation** (`*.md`, `*.csv`, `*.json`): CC BY 4.0.

You are free to reuse and adapt these materials with attribution.

---

## Contributing

This repository accompanies a peer-reviewed manuscript and primarily serves reproducibility. We welcome:

- **Issues** reporting errors in scoring, data, or documentation.
- **Pull requests** that extend the corpus, add new benchmarks, or refine operational indicators.
- **Discussions** on alternative weighting schemes, dimension definitions, or methodology improvements.

For substantive changes (e.g., revising the rubric), please open an issue first to discuss the proposed change.

---

## Contact

**Rubén Gómez** — `ruben.cicata@gmail.com`
CICATA-Querétaro, Instituto Politécnico Nacional

For questions about the paper, framework methodology, or to report issues with reproducibility, please open a GitHub issue or contact directly.

---

## Acknowledgments

We thank the three independent evaluators who participated in the BQAI scoring exercise, the authors of the original benchmarks evaluated in this work, and the Instituto Politécnico Nacional and Universidad Autónoma de Querétaro for institutional support.
