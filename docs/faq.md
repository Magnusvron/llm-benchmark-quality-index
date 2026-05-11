# Frequently Asked Questions

## About the BQAI framework

### Why does the BQAI exist?

LLM benchmarks vary enormously in scientific quality. Some are saturated. Some are contaminated. Some have inconsistent splits across studies. The BQAI is a quantitative framework for assessing whether a benchmark is a sound scientific instrument, separately from how popular it is.

A common confusion: BQAI does **not** measure how hard or discriminative a benchmark is. A benchmark can score high on BQAI but be near saturation (e.g., MMLU-Pro), or score low on BQAI but remain widely used (e.g., MMLU). BQAI assesses **methodology**, not difficulty.

### Why is reproducibility weighted so heavily (Q4 = 0.349)?

Irreproducible benchmarks cannot support cumulative scientific progress. If you cannot independently verify a reported number, the benchmark is not a scientific instrument — it is a marketing claim. Reproducibility is therefore weighted as the single most important dimension, with the heaviest weight reflecting that priority.

The weight derivation follows the Analytic Hierarchy Process (AHP) under the principle of **Scientific Reproducibility Priority**, formalized in the pairwise comparison matrix in `04_bqai/ahp_weights.py`.

### Why use AHP for weights instead of equal-weighting?

Equal-weighting (w = 1/7 for each dimension) assumes all quality dimensions matter equally, which is empirically false: irreproducibility makes a benchmark useless regardless of other strengths, while a low coverage score can still leave a benchmark useful for its narrower purpose.

AHP allows us to formalize relative priorities through a structured procedure (pairwise comparisons, consistency verification) that is auditable and defensible. The sensitivity analysis (`04_bqai/sensitivity_analysis.py`) demonstrates that BQAI tier assignments are robust to weight perturbations up to ±50% — so the choice of weights matters at the margins but not for the main conclusions.

### Are the weights "correct"?

No single weighting is universally correct. The current weights reflect the priorities for **frontier LLM evaluation in 2026** (reproducibility and contamination resistance as central concerns). Different research contexts may warrant different weights:
- Safety-focused research → elevate Q7
- Cognitive science research → elevate Q6
- Equity research → elevate Q7

The framework is **transparent**: we publish the AHP matrix, the rubric, and the code. Anyone can apply alternative weights and re-compute the BQAI.

## About the sample of 30 benchmarks

### Why only 30 of the 63 benchmarks in the corpus?

Three reasons:
1. **Documentation quality:** Several benchmarks in the corpus lack the public documentation needed to score certain dimensions (e.g., very recent Emerging Track benchmarks without IAA documentation).
2. **Diminishing returns:** Going from 30 to 63 would add scoring effort proportional to the addition (~10% increase per evaluator), but the marginal increase in analytical insight is small.
3. **Sample representativeness:** 30 benchmarks already cover all six dimensions with ≥ 4 each, the full track diversity, and 70% of the 20 subcategories. The representativeness analysis (`06_corpus/representativeness_analysis.md`) demonstrates the sample mirrors the corpus's structural properties.

### Why expand from the original 21 to 30?

The original 21-benchmark sample under-represented D4 (Agency) and D5 (Safety) — exactly the dimensions the paper identifies as having the most critical evaluation gaps. The expansion to 30 brings each dimension to ≥ 4 benchmarks and addresses this internal incoherence with the paper's own argument.

### Could the conclusions change if you scored all 63?

Likely no, but we cannot prove it without doing so. The representativeness analysis shows the sample preserves the corpus's structural properties, so the **distributional conclusions** (proportion of benchmarks in each tier, etc.) should generalize. **Individual rankings** are exact for the 30 scored benchmarks; for the 33 unscored, only their qualitative position can be inferred.

## About inter-rater reliability

### Why use three evaluators instead of two?

Two-evaluator IAA is limited: you get one pairwise correlation per dimension. Three evaluators give three pairwise correlations and allow ICC(2,k) with absolute-agreement, which is the standard psychometric metric. Three is the minimum recommended sample size for ICC reporting.

### What if the IAA comes back low?

Low IAA (e.g., ICC < 0.60) would indicate genuine ambiguity in the rubric, not just evaluator variance. The response would be:
1. Identify which dimensions have the lowest agreement.
2. Tighten the operational indicators in `01_rubric/BQAI_rubric_full.md` for those dimensions.
3. Schedule a calibration discussion among evaluators.
4. Re-score the problematic dimensions.

We expect IAA to be in the **good to excellent range** (ICC ≥ 0.75, weighted κ ≥ 0.60) based on:
- The structured rubric with verifiable indicators
- The blinded protocol
- The evaluators' shared expertise in LLM methodology

### Why are scores reconciled after IAA computation?

This is the standard psychometric protocol:
1. **Raw scores** preserve the agreement signal (used for IAA computation).
2. **Reconciled scores** improve methodological soundness (used for final BQAI).

Both are released in the repository to maintain full transparency.

## About the performance matrix

### Why are some cells in the performance matrix empty?

Because the model developer never reported that score. We do not fill in cells with values from non-authoritative sources (e.g., third-party leaderboards with inconsistent methodology). An empty cell is more honest than a misleading number.

### Will the matrix become outdated?

Yes, rapidly. New models are released monthly. The `05_performance_matrix/sources_detailed.csv` includes an `access_date` column to make outdating visible. The repository structure allows community contributions (pull requests) to add new model-benchmark scores as they appear.

### Why don't you report your own evaluations?

Two reasons:
1. **Cost:** Running 16 frontier models on 10 benchmarks would cost tens of thousands of dollars in API fees.
2. **Calibration:** Model developers know their models best and have optimal evaluation infrastructure. Reproducing their reported numbers (with documented source) is more reliable than re-running with our own (potentially suboptimal) settings.

## About this repository

### Why is the code dual-licensed?

- **MIT for code** maximizes reusability (anyone can build commercial tools on top).
- **CC-BY-4.0 for data and rubric** is the standard for academic datasets and requires attribution but allows derivative work.

### Can I use this for my own benchmark assessment?

Yes — that is the intended use. You can:
1. Score additional benchmarks using `01_rubric/BQAI_rubric_full.md`.
2. Apply alternative weights via `04_bqai/compute_bqai.py`.
3. Extend the corpus by adding rows to `06_corpus/benchmarks_63.csv`.

We welcome pull requests for these extensions.

### How do I cite this work?

See `CITATION.cff` (machine-readable) or the citation block in `README.md` (BibTeX).

### Is there a DOI?

Yes — the repository is archived on Zenodo with a permanent DOI. See the badge in `README.md` (added after first Zenodo release).

## Methodology critique

### Isn't the BQAI itself subjective?

Yes, partially. The AHP pairwise comparisons reflect human judgment about what matters in LLM evaluation. The rubric scoring requires evaluator judgment about whether evidence is sufficient. We mitigate this by:
1. **Documenting the rubric** with verifiable indicators (not arbitrary judgments).
2. **Using multiple evaluators** with blinded protocol.
3. **Reporting IAA** to quantify residual subjectivity.
4. **Sensitivity analysis** to show conclusions are robust to weight choices.

The alternative — refusing to assess benchmark quality at all because some subjectivity is unavoidable — would leave the field with no way to distinguish rigorous instruments from popular but flawed ones.

### Are there alternatives in adjacent literatures?

Yes. Educational psychometrics has decades of work on test quality assessment. Software benchmarking (SPEC, MLPerf) has methodological frameworks. The BQAI builds on these traditions while adapting to the specific concerns of LLM evaluation (contamination, saturation, rapidly evolving capabilities).

The paper's §2 (Related Work) discusses these connections; the BQAI is not the first quantitative quality assessment framework, but it is the first specifically designed for LLM benchmarks with AHP-derived weights and Monte Carlo sensitivity validation.
