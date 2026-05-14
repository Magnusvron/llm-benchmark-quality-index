# BQAI Operational Scoring Rubric — Full Specification

> This document expands Table 7 of the paper into evidence-based, observable indicators. The goal is to minimize subjective judgment by anchoring each scoring decision to verifiable artifacts (papers, repositories, leaderboards, documentation).

## Scoring scale

Scores are continuous in `[0.00, 1.00]` with four reference tiers:

| Tier | Range | Interpretation |
|------|-------|----------------|
| Low | 0.00 – 0.30 | Substantial absence of evidence; minimal documentation; saturated or unreproducible. |
| Moderate | 0.31 – 0.60 | Partial evidence; some best practices implemented; gaps remain. |
| High | 0.61 – 0.80 | Solid evidence; documented protocols; meets community best practices. |
| Excellent | 0.81 – 1.00 | Gold-standard practices; comprehensive evidence; minimal weaknesses. |

**Use of intermediate values:** Evaluators may assign any value in [0, 1]. Use intermediate values (e.g., 0.75) when evidence partially satisfies adjacent tiers.

---

## Q1 — Annotation Quality and Consistency (weight: 0.213)

**What this measures:** Rigor of the annotation pipeline, expertise of annotators, inter-annotator agreement (IAA), and systematic quality control. Captures whether labels and ground-truth answers are trustworthy.

### Observable indicators

| Score | Evidence required (verifiable) |
|-------|--------------------------------|
| **0.00 – 0.30 (Low)** | No documented annotation protocol. No information about who created the labels or how. No quality control. No IAA reported. |
| **0.31 – 0.60 (Moderate)** | Single annotator OR minimal documentation. Basic checks (e.g., spot-checks) but no formal IAA. Mention of "expert review" without specifics. |
| **0.61 – 0.80 (High)** | Multiple annotators with documented expertise (e.g., "graduate students in CS"). IAA reported and ≥ 0.70 (Cohen's κ, ICC, or equivalent). At least one quality control step documented (e.g., adjudication of disagreements). |
| **0.81 – 1.00 (Excellent)** | Multi-stage expert pipeline. IAA ≥ 0.80 reported. Systematic validation: expert verification at multiple checkpoints, independent review, error analyses, published annotation guidelines. |

### Where to look
- Original benchmark paper, sections on "Dataset Construction" or "Annotation"
- Supplementary materials / appendices
- Project website's "About the data" or "Methodology" pages
- Dataset cards on HuggingFace (look for "Curation Rationale" and "Annotations" sections)

### Common pitfalls
- **Do not assume rigor.** If no IAA is reported, do not give the benefit of the doubt — score Moderate or lower.
- A benchmark may have "PhD-level questions" but if the *answers* were not validated by multiple experts, Q1 is not automatically High.
- Crowdsourced datasets without redundancy controls (multiple workers per item) should not exceed Moderate.

### Examples
- **High Q1 (~0.85):** SWE-bench Verified — expert software engineers reviewed each problem, multi-annotator validation, public discussion of disagreements.
- **Moderate Q1 (~0.55):** MMLU — multiple authors compiled questions but no formal IAA reported; questions sourced from various exam materials with inconsistent validation depth.
- **Low Q1 (~0.30):** Older benchmarks that aggregate questions from web sources without documented validation.

---

## Q2 — Instructional Clarity and Format Consistency (weight: 0.073)

**What this measures:** Whether tasks are unambiguously defined, prompt templates are standardized, and input/output specifications are clear enough to prevent format-driven shortcuts or evaluator confusion.

### Observable indicators

| Score | Evidence required |
|-------|-------------------|
| **0.00 – 0.30 (Low)** | Task definitions are ambiguous. No standardized prompt template. Format varies across instances. Different papers report different prompt formulations for the same benchmark. |
| **0.31 – 0.60 (Moderate)** | Tasks defined but format conventions left to the evaluator. Users must infer how to prompt. Some examples shown but no canonical template. |
| **0.61 – 0.80 (High)** | Clear input/output specifications. Documented prompt structure with at least one canonical template. Minimal ambiguity in expected output format. |
| **0.81 – 1.00 (Excellent)** | Fully specified prompt templates. Comprehensive documentation of all valid formats. Format-robustness studies published. Schema/grammar enforced on outputs. |

### Where to look
- Benchmark paper's "Evaluation Protocol" or "Task Formulation" section
- GitHub repo's `prompts/`, `templates/`, or `eval_config.json`
- Official evaluation harness (e.g., LM Evaluation Harness configurations)

### Examples
- **Excellent (~0.95):** IF-Eval — verifiable constraints with formal schema; format-robust by design.
- **High (~0.80):** HumanEval — clear function signature + docstring + tests, standardized.
- **Moderate (~0.60):** Chatbot Arena — natural conversation, no fixed template (which is intentional but lowers Q2).

---

## Q3 — Standardization and Versioning Practices (weight: 0.117)

**What this measures:** Whether the benchmark has a frozen test set, documented splits, semantic versioning, and contamination-resistance mechanisms. Essential for longitudinal comparability.

### Observable indicators

| Score | Evidence required |
|-------|-------------------|
| **0.00 – 0.30 (Low)** | No versioning. Train/val/test splits inconsistent across studies. Test set has changed over time without documentation. No leaderboard or governance. |
| **0.31 – 0.60 (Moderate)** | Ad hoc splits in informal documentation. Some versioning but inconsistent (e.g., "v1.1" mentioned in commits but no formal release). |
| **0.61 – 0.80 (High)** | Frozen test set explicitly identified. Documented partitions (train/val/test) with sizes. Clear version naming convention. Some form of public leaderboard or release notes. |
| **0.81 – 1.00 (Excellent)** | Semantic versioning (v1.0.0). Formal changelog. Public leaderboard with version tags. Contamination-resistant design (rolling updates, held-out test set, cryptographic commitment, expert review). Released artifacts with checksums. |

### Where to look
- GitHub releases page
- Hugging Face dataset versions
- Leaderboard with version filters (e.g., LiveBench, Papers with Code)
- CITATION.cff, CHANGELOG.md

### Examples
- **Excellent (~0.95):** LiveBench — versioned monthly releases, transparent rolling updates.
- **High (~0.85):** MMLU-Pro — frozen test set, documented splits, public leaderboard.
- **Low (~0.30):** Datasets where different papers report different test sizes for the "same" benchmark.

---

## Q4 — Reproducibility and Baseline Implementations (weight: 0.349) ⭐ Heaviest weight

**What this measures:** Whether independent researchers can reproduce reported numbers. Includes availability of evaluation scripts, deterministic scoring, documented metrics, and hyperparameter transparency.

### Observable indicators

| Score | Evidence required |
|-------|-------------------|
| **0.00 – 0.30 (Low)** | No code released. Metrics undefined or vague ("we used accuracy" without specifying what counts as correct). Impossible to reproduce reported numbers from documentation alone. |
| **0.31 – 0.60 (Moderate)** | Partial scripts available. Some metric definitions but missing hyperparameters (temperature, seed, prompt formatting). Reproduction requires significant guesswork. |
| **0.61 – 0.80 (High)** | Official evaluation scripts published. Metrics formally defined (e.g., Pass@k with exact formula). Common hyperparameters documented. Reproduction achievable with reasonable effort. |
| **0.81 – 1.00 (Excellent)** | Deterministic pipeline (fixed seeds, documented). Reported variance ≤ ±0.5%. Containerized evaluation (Docker, Singularity). Complete hyperparameter specification. Continuous integration on benchmark scripts. |

### Where to look
- GitHub repo for `eval.py`, `evaluate.py`, or `run_eval.sh`
- README "Reproducing our results" sections
- Dockerfile or `environment.yml`
- Reported configurations (e.g., LM Evaluation Harness configs)

### Examples
- **Excellent (~1.00):** HELM — containerized, deterministic, fully versioned scripts.
- **High (~0.85):** HumanEval — official `human-eval` package with Pass@k computation.
- **Moderate (~0.60):** Benchmarks where the eval script exists but lacks documented hyperparameters.

---

## Q5 — Robustness to Prompt Variation and Contamination (weight: 0.167)

**What this measures:** Resistance to format sensitivity, prompt engineering artifacts, and training data leakage. Critical in 2025+ when training corpora subsume most public test sets.

### Observable indicators

| Score | Evidence required |
|-------|-------------------|
| **0.00 – 0.30 (Low)** | Severe prompt sensitivity documented OR confirmed contamination in major model training corpora OR saturated (state-of-the-art > 95%). Performance varies > 10% between equivalent prompts. |
| **0.31 – 0.60 (Moderate)** | Some format sensitivity acknowledged. Contamination concerns raised but not mitigated. State-of-the-art 90–95% (approaching ceiling). No active anti-contamination mechanism. |
| **0.61 – 0.80 (High)** | Adversarial filtering OR expert validation reduces shortcuts. State-of-the-art < 92%. Documented robustness checks. Some form of perturbation analysis. |
| **0.81 – 1.00 (Excellent)** | Rolling updates (monthly/quarterly) OR unpublished held-out test set OR cryptographic commitment scheme. State-of-the-art < 90%. Documented contamination-detection tools. Adversarial robustness studies published. |

### Where to look
- Benchmark paper's "Limitations" or "Contamination" sections
- Updates/changelog showing rolling refreshes
- Public leaderboards showing top scores (saturation check)
- Independent contamination studies (e.g., Golchin & Surdeanu 2024, Zhang et al. 2024)

### Anti-contamination mechanisms (any of these → score higher)
- **Rolling updates:** LiveBench (monthly), LiveCodeBench (quarterly)
- **Unpublished problems:** FrontierMath, HLE (private test set)
- **Adversarial filtering:** WinoGrande (Adversarial Winograd)
- **Expert validation post-hoc:** SWE-bench Verified
- **Format diversity audits:** HELM

### Examples
- **Excellent (~0.95):** LiveBench, FrontierMath — active contamination resistance.
- **Moderate (~0.50):** Older static benchmarks without anti-contamination mechanisms.
- **Low (~0.20):** GLUE — severely saturated and contaminated.

---

## Q6 — Cognitive Skill Coverage and Task Diversity (weight: 0.033)

**What this measures:** Breadth of cognitive abilities assessed. A narrower but rigorous benchmark is preferred over a broad but methodologically weak one, hence the low weight.

### Observable indicators

| Score | Evidence required |
|-------|-------------------|
| **0.00 – 0.30 (Low)** | Single narrow task (e.g., 4th-grade arithmetic only). One cognitive ability tested. |
| **0.31 – 0.60 (Moderate)** | 2–3 related subtasks within a single cognitive area (e.g., 3 types of math reasoning). |
| **0.61 – 0.80 (High)** | ≥ 3 distinct cognitive skills OR broad domain coverage (e.g., 30+ subjects in MMLU). |
| **0.81 – 1.00 (Excellent)** | ≥ 5 cognitive dimensions OR 10+ diverse tasks. Multi-skill integrative design. Cross-domain assessment. |

### Examples
- **Excellent (~0.95):** HELM (~40 scenarios), BIG-bench (200+ tasks).
- **High (~0.90):** MMLU (57 subjects), MMMU (30 disciplines).
- **Low (~0.35):** GSM8K (grade-school arithmetic only).

---

## Q7 — Bias Mitigation and Cross-Cultural Validity (weight: 0.048)

**What this measures:** Whether the benchmark addresses linguistic diversity, demographic representation, and generalization beyond WEIRD (Western, Educated, Industrialized, Rich, Democratic) populations.

### Observable indicators

| Score | Evidence required |
|-------|-------------------|
| **0.00 – 0.30 (Low)** | English-only. No bias analysis. Assumes Western academic context throughout. |
| **0.31 – 0.60 (Moderate)** | Multilingual support OR some bias mention, but no systematic audit. Demographic considerations limited to one dimension. |
| **0.61 – 0.80 (High)** | Documented bias analysis (e.g., demographic breakdown of accuracy). Multilingual coverage with attention to fairness. At least 2 cultural contexts. |
| **0.81 – 1.00 (Excellent)** | Cross-cultural validation across ≥ 3 typologically diverse languages. Demographic audits with published mitigation protocols. Bias testing as a primary methodology, not an afterthought. |

### Where to look
- "Limitations" and "Ethical Considerations" sections of papers
- Datasheets for Datasets documentation
- Hugging Face dataset cards' "Considerations for Using the Data"

### Examples
- **High (~0.80):** C-Eval — explicitly Chinese-language, cross-cultural by design within Chinese context.
- **Moderate (~0.55):** TruthfulQA — addresses Western misconceptions; some cultural diversity but English-only.
- **Low (~0.30):** Most English-only benchmarks without bias analyses.

---

## Computing the final BQAI score

After scoring all seven dimensions:

```
BQAI = 0.349·Q4 + 0.213·Q1 + 0.167·Q5 + 0.117·Q3 + 0.073·Q2 + 0.048·Q7 + 0.033·Q6
```

Classify into tiers:

```
Tier A: BQAI ≥ 0.82
Tier B: 0.70 ≤ BQAI < 0.82
Tier C: BQAI < 0.70
```

---

## Reconciliation protocol (for multi-evaluator scoring)

When multiple evaluators score the same benchmark, the recommended reconciliation procedure is:

1. **Compute per-evaluator BQAI independently** before any discussion.
2. **Report raw scores** in `02_scoring/raw_scores/` (pre-reconciliation).
3. **Compute inter-rater reliability metrics** (ICC, weighted Cohen's κ) on raw scores.
4. **For dimensions with > 0.20 absolute difference between evaluators**, schedule a reconciliation discussion:
   - Each evaluator presents the evidence supporting their score.
   - Reference the operational indicators in this rubric.
   - Reach consensus or, if unresolved, use the median.
5. **Document reconciliation decisions** in `02_scoring/reconciliation_log.md`.
6. **Use reconciled (post-consensus) scores** as the final BQAI input.

This protocol preserves both the formal IAA evidence (computed on raw scores) and the methodological soundness of final scores (computed on reconciled scores).
