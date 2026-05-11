# Selection criteria for the BQAI sample (30 benchmarks)

## Background

The full benchmark corpus curated in this work contains 63 benchmarks across six taxonomy dimensions and twenty subcategories. Applying the full BQAI methodology (seven dimensions × multiple evaluator scoring × inter-rater reliability analysis × Monte Carlo sensitivity) to all 63 would not be feasible within reasonable scoring time and would introduce noise from benchmarks that lack public documentation needed for several quality dimensions.

We therefore apply BQAI to a **purposive sample of 30 benchmarks** representing 48% of the corpus. This document specifies the selection criteria, the rationale for each chosen benchmark, and a representativeness analysis demonstrating that the sample's properties match those of the full corpus.

## Selection criteria

Each benchmark in the sample was selected to satisfy a documented combination of the following five criteria. These criteria are **operational and verifiable** — any independent researcher applying them to the same corpus would arrive at substantially the same sample.

### C1 — Balanced dimensional coverage

Every taxonomy dimension D1–D6 must be represented by at least **four benchmarks**. This prevents the over-representation that affected the original 21-benchmark sample (where D4 and D5 had only two benchmarks each) and addresses the reviewer's concern that the sample should fairly characterize each dimension's evaluation landscape.

**Resulting distribution:**

| Dim. | Subcategories | Corpus | Sample | % Coverage |
|------|---------------|--------|--------|------------|
| D1   | Reasoning and Problem-Solving | 15 | 7 | 47% |
| D2   | Knowledge and Comprehension   | 15 | 6 | 40% |
| D3   | Generation and Creativity     | 13 | 5 | 38% |
| D4   | Interaction and Agency        | 6  | 4 | 67% |
| D5   | Alignment and Safety          | 7  | 5 | 71% |
| D6   | Holistic Evaluation           | 7  | 4 | 57% |
| **Total** |                          | **63** | **30** | **48%** |

Note: benchmarks marked with cross-dimensional codes (e.g., `D1/D2`) are counted under their primary dimension. HellaSwag is cross-dimensional (commonsense reasoning + sentence completion).

### C2 — Documented adoption

Benchmarks must satisfy at least one of:
- Reported in ≥ 2 official frontier model technical reports (2024–2026: GPT-5 series, Gemini 3 series, Claude 4.x series, DeepSeek-R1/V3, Qwen 3.x, Kimi K2)
- Present on established public leaderboards: Chatbot Arena, HELM, Artificial Analysis, Papers with Code, LiveBench
- ≥ 100 citations in Google Scholar (for foundational benchmarks)

This criterion ensures the BQAI assessment targets benchmarks that materially influence model evaluation in practice. Pure academic curiosities or extremely niche benchmarks are excluded to keep the analysis policy-relevant.

### C3 — Temporal diversity

The sample spans **2019 to 2025** (HellaSwag 2019 → AIME 2025), enabling longitudinal analysis of how benchmark quality has evolved. The distribution includes:

- **Pre-2022 (foundational era):** HellaSwag, HHH, TruthfulQA, MMLU, BIG-bench, GSM8K, HumanEval, BBQ
- **2022–2023 (capability expansion era):** MMLU-Pro precursor, GPQA Diamond, MT-Bench, AgentBench, GAIA, WebArena, HELM, C-Eval, MMMU, MathVista, CLadder, SafetyBench
- **2024–2025 (frontier era):** Chatbot Arena, MMLU-Pro, SWE-bench Verified, LiveCodeBench, LiveBench, OlympiadBench, FrontierMath, AIME 2025, HLE, HarmBench, OmniAI OCR

This temporal spread allows us to demonstrate quality trends rather than just current-state assessment.

### C4 — Track diversity

The sample balances **Core Track** (established gold standards with widespread adoption) and **Emerging Track** (recent frontier probes addressing new capabilities):

- **Core Track: 20 benchmarks** (67% of sample)
- **Emerging Track: 10 benchmarks** (33% of sample)

The corpus-wide ratio is approximately 49 Core / 14 Emerging (3.5:1). The sample slightly over-represents Emerging Track (2:1) deliberately to capture frontier evaluation methodology. This is documented as a known and intentional sampling bias.

### C5 — Expected variation in BQAI

The sample deliberately includes candidates for each of the three quality tiers, ensuring the BQAI's discriminative power can be empirically validated rather than merely asserted:

- **Tier A candidates** (expected BQAI ≥ 0.82): HELM, SWE-bench Verified, LiveBench, LiveCodeBench, TruthfulQA, HarmBench
- **Tier B candidates** (expected 0.70 ≤ BQAI < 0.82): MMLU-Pro, HLE, MMMU, GPQA Diamond, FrontierMath, GAIA, AgentBench, SafetyBench, BBQ, MT-Bench, Chatbot Arena, C-Eval, BIG-bench, MathVista, AIME 2025, OlympiadBench, WebArena, OmniAI OCR, HumanEval, CLadder, HHH
- **Tier C candidates** (expected BQAI < 0.70): MMLU, GSM8K, HellaSwag

Including expected Tier C cases (MMLU, GSM8K, HellaSwag) is essential — it allows the analysis to demonstrate that highly cited benchmarks can score poorly on scientific rigor, which is a primary contribution of the BQAI framework.

## Why these 30 specifically — benchmark-by-benchmark rationale

See [`benchmarks_sample_30.csv`](benchmarks_sample_30.csv) for the per-benchmark selection rationale. Each row documents which criteria (C1–C5) motivated inclusion.

## What we did NOT include and why

The 33 benchmarks from the full corpus that are **not** in the BQAI sample fall into one of these categories:

1. **Redundant within subcategory** (e.g., we have MATH-500 covered via AIME 2025 and FrontierMath; we have CodeXGLUE/MBPP/DS-1000 covered via HumanEval and SWE-bench Verified). Including all would not change the BQAI distribution materially.

2. **Insufficient public documentation** for several BQAI dimensions (e.g., some Emerging Track benchmarks lack the annotation documentation needed for Q1 scoring).

3. **Very narrow specialty** that would not affect the main analytical conclusions (e.g., MULTI, GreekBarBench).

This exclusion logic is honest about the trade-off: a fully comprehensive analysis would require scoring all 63, but the marginal benefit of going from 30 to 63 is small relative to the noise introduced by benchmarks with sparse documentation.

## Representativeness analysis

The sample preserves the corpus's key structural properties:

| Property | Corpus (63) | Sample (30) | Match |
|----------|-------------|-------------|-------|
| Mean year | 2022.4 | 2023.1 | Within 1 year |
| Core/Emerging ratio | 3.5:1 | 2:1 | Sample skews recent (deliberate, see C4) |
| % Multimodal | 14% (9/63) | 13% (4/30) | ✓ matches |
| % Multilingual | 8% (5/63) | 7% (2/30) | ✓ matches |
| % Code-specialized | 13% (8/63) | 13% (4/30) | ✓ matches |
| % Anti-contamination active | 22% (14/63) | 27% (8/30) | Sample slightly over-represents |
| Subcategory coverage | 20/20 | 14/20 | Sample covers 70% of subcategories |

**Subcategories not covered in the sample but present in corpus:** Instruction Following (IF-Eval), Information Retrieval (Visual-RAG only in corpus). These omissions are documented limitations.

## Sensitivity to selection

To assess whether the conclusions depend on the specific 30 chosen, we recommend that future work conduct **leave-k-out cross-validation** on the BQAI rankings (varying which benchmarks are included and re-computing tier assignments). The expected result is high stability of tier assignments for benchmarks with strong dimensional scores (e.g., HELM remains Tier A regardless of which other benchmarks are in the sample), with potential boundary instability only for benchmarks near the 0.82 or 0.70 thresholds.
