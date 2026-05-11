# 05_performance_matrix/ — Model × benchmark performance matrix with source traceability

This directory contains the consolidated performance matrix (16 models × 10 benchmarks reported in the paper) with **complete source traceability** for every reported score.

## Contents (populated in Session 3)

| File | Description |
|------|-------------|
| `performance_matrix.csv` | The matrix in tidy long-format: model, benchmark, score, source_type, source_url, access_date, settings. |
| `sources_detailed.csv` | Full per-score traceability: benchmark version, reasoning_effort setting, tool_use setting, shot count, temperature, notes. |
| `README.md` | This file. |

## Schema of `sources_detailed.csv`

| Column | Description |
|--------|-------------|
| `model` | Model name (e.g., "GPT-5.4", "Claude Opus 4.6", "DeepSeek-R1") |
| `model_version` | Specific version/checkpoint if applicable |
| `benchmark` | Benchmark name (e.g., "MMLU-Pro", "SWE-bench Verified") |
| `benchmark_version` | Specific version of the benchmark used |
| `score` | Reported score (typically percentage) |
| `source_type` | One of: `official_report`, `leaderboard`, `peer_reviewed`, `industry_blog` |
| `source_url` | Direct URL to the source |
| `access_date` | YYYY-MM-DD when the score was retrieved |
| `reasoning_effort` | "high", "medium", "low", "extended thinking", or "default" |
| `tool_use` | "yes" / "no" and which tools (e.g., "yes - Python interpreter") |
| `shot_count` | "0-shot", "5-shot", "few-shot" with k value |
| `temperature` | Reported sampling temperature, if available |
| `notes` | Free-text caveats (e.g., "score with parallel test-time compute") |

## Source-type hierarchy

When multiple sources report a score for the same model-benchmark pair, we prioritize in this order:

1. **`official_report`** (most authoritative): Official technical reports or model release announcements from the developer (OpenAI, Anthropic, Google DeepMind, Meta, xAI, DeepSeek, Qwen, Moonshot AI).
2. **`leaderboard`**: Established public leaderboards with documented methodology (Chatbot Arena/LMArena, HELM, Artificial Analysis, LLM-Stats, Papers with Code).
3. **`peer_reviewed`**: Peer-reviewed papers with independent evaluation (third-party verification).
4. **`industry_blog`** (lowest authority): Vendor blog posts or marketing materials not formally peer-reviewed.

Each score's source type is documented to allow readers to weight the evidence appropriately.

## How this addresses reviewer comments

This addresses **Reviewer 2, Comment 2**:

> "every reported score should be traceable to a precise source. The manuscript should provide exact references for each model-benchmark score, including the benchmark version, date of access, evaluation setting, reasoning-effort setting where relevant, tool-use setting, and whether the score comes from an official report, a leaderboard, or an independent evaluation."

The `sources_detailed.csv` provides exactly this level of granularity for all ~160 cells in the performance matrix.

## Limitations acknowledged

- **Rapidly evolving landscape:** Scores reflect publicly reported values as of March 2026. Future model releases will require updates.
- **Heterogeneous reporting:** Frontier model providers report benchmarks inconsistently. Some scores are missing because the model developer never published them, not because we omitted them.
- **Reasoning-effort settings:** Different providers use different terminology ("high", "thinking mode", "extended test-time compute"). We document the provider's terminology and explain equivalences where possible.

## Status

🟡 **To be built in Session 3.** This is the most labor-intensive component (~160 cells × verification effort each). The structure and schema are documented above; data compilation pending.
