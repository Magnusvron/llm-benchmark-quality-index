# 05_performance_matrix/ — Source traceability for the performance matrix

This directory provides per-cell traceability for every score reported in the performance matrix of the accompanying paper (Tables 4, 5, 6). Each of the 160 (model, benchmark) cells—including the 51 cells marked as not reported—is documented with its primary source, evaluation configuration, and access date.

## Contents

| File | Description |
|------|-------------|
| `sources_detailed.csv` | The complete 160-row traceability table with 20 fields per cell. |
| `performance_matrix_base.csv` | The reconstructed performance matrix in long format (model × benchmark, with scores or null markers). |

## Source-priority hierarchy

Every cell is classified by source type using the four-tier hierarchy documented in Appendix B of the paper:

1. **Official technical reports and model system cards** from the model developer (`source_type: official_report`) — the primary authoritative source for a model's own claimed performance. 93 of the 109 reported scores (85%) come from this tier.

2. **Established public leaderboards** with documented methodology (`source_type: leaderboard`) — used as primary source when the benchmark is structurally external to the developer (all Arena Elo Rank values come from LMArena, 16 of 109 reported scores) and as cross-reference for corroboration.

3. **Peer-reviewed publications with independent third-party evaluation** (`source_type: peer_reviewed`) — take precedence over vendor blog posts when independent corroboration matters.

4. **Vendor blog posts** (`source_type: vendor_blog`) — used only when no higher-priority source is available, always flagged in `notes`. No score in the current matrix relies exclusively on tier-(iv) sources.

Cells that cannot be traced to a public document are recorded as `source_type: not_reported` rather than estimated.

## Field reference

Each row in `sources_detailed.csv` has the following 20 fields:

**Model identification:**
- `model` — display name as in the paper (e.g., "Claude Opus 4.6")
- `developer` — organization (OpenAI, Anthropic, Google DeepMind, Meta, DeepSeek, Alibaba/Qwen, Moonshot AI, xAI)
- `model_category` — `frontier_proprietary` | `longitudinal_baseline` | `open_source`
- `extended_test_time_compute` — boolean; `true` for models marked with † in the paper

**Benchmark identification:**
- `benchmark` — name as in the paper (e.g., "GPQA Diamond")
- `benchmark_metric` — accuracy, pass@1, resolved_pct, rank
- `benchmark_domain` — D1_Reasoning, D2_Knowledge, D3_Code, D1_Math, D2_Expert, D3_Language
- `benchmark_version` — version string where applicable (e.g., "v1.0, 12,032 questions, 10 options" for MMLU-Pro)
- `benchmark_canonical_url` — authoritative URL for the benchmark (typically GitHub or paper)

**Score and source:**
- `score` — numeric value as reported (blank if `reported=no`)
- `reported` — yes / no
- `source_type` — `official_report` | `leaderboard` | `peer_reviewed` | `vendor_blog` | `not_reported`
- `source_url` — URL of the primary public document for this score
- `cross_reference_url` — independent corroborating leaderboard URL when available

**Evaluation configuration:**
- `reasoning_effort` — preserved using each developer's original terminology (e.g., "high" for OpenAI, "extended_thinking" for Anthropic/Google, "adaptive_max" for newer Claude, "thinking_mode" for Qwen/DeepSeek)
- `tool_use` — default / none / varies_per_benchmark / etc.
- `shot_count` — 0-shot, 5-shot, avg@8, avg@32, etc.
- `temperature` — value or "default"

**Audit trail:**
- `access_date` — 2026-05-10 for the current matrix snapshot
- `notes` — caveats, methodological notes, or specific configuration details from the primary source

## Headline statistics

- **160 total cells** (16 models × 10 benchmarks)
- **109 reported cells** (68% coverage)
- **51 not-reported cells** (32%) explicitly documented rather than estimated
- **93 official-report sources** (85% of reported)
- **16 leaderboard sources** (15% of reported, primarily Arena Elo Rank)
- **0 vendor-blog-only sources**

## Use cases

The CSV is structured to support multiple workflows:

1. **Verification:** Any reader can check a specific cell of the performance matrix by looking up the corresponding row in `sources_detailed.csv` and following the `source_url`.

2. **Methodological audit:** The `reasoning_effort`, `tool_use`, and `shot_count` fields allow assessment of whether scores are comparable across models—for instance, identifying that Anthropic's "adaptive_max" trial-averaging may not be directly comparable to OpenAI's single-pass "high" reasoning.

3. **Update propagation:** As newer model releases or corrected reports become available, individual cells can be updated by editing the corresponding row, preserving the audit trail in `access_date` and `notes`.

4. **Extension:** Researchers can extend the matrix to additional models or benchmarks by appending rows with the same schema.

## Acknowledged limitations

We do not independently re-run every model on every benchmark, as closed-weight frontier models are typically accessible only through paid APIs and many reported configurations require substantial compute. Three mitigations are documented in Appendix B of the paper:

- Leaderboard cross-references (Artificial Analysis, LMArena, LiveCodeBench) are recorded where available.
- The complete configuration fields preserve methodological detail that would be lost in an unsourced score.
- Cells without a traceable primary source are excluded rather than estimated.

## Regenerating

The scripts that produced these CSVs are in this directory's parent workspace (not committed to the repository to keep the artifact-vs-tool distinction clean); the structure can be regenerated from the paper's Tables 4–6 plus the source list documented in Appendix B.
