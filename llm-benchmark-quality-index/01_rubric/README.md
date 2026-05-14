# 01_rubric/ — Operational scoring rubric

This directory contains the full operational rubric used to score benchmarks against the seven BQAI quality dimensions (Q1–Q7).

## Contents

| File | Description |
|------|-------------|
| `BQAI_rubric_full.md` | Complete rubric with evidence-based indicators, tier definitions, examples, and reconciliation protocol. The authoritative reference for evaluators. |
| `operational_indicators.csv` | Machine-readable version of the rubric indicators (one row per dimension × tier). Useful for programmatic checks. |

## How to use

For **scoring a benchmark**: read `BQAI_rubric_full.md` once to internalize the four tiers (Low / Moderate / High / Excellent), then score each dimension by matching observable evidence to the indicators.

For **programmatic validation**: use `operational_indicators.csv` to check whether assigned scores are consistent with documented evidence (e.g., flag scores in the "Excellent" tier that lack documentation of multi-stage expert validation).

## Key principle

The rubric is designed to **minimize subjective judgment** by anchoring each scoring decision to verifiable artifacts: papers, repositories, leaderboards, dataset cards, official documentation. When evaluators disagree, they should resolve the disagreement by jointly inspecting the evidence cited in the rubric, not by debating preferences.

## Reference

This rubric expands Table 7 of the paper. The weight derivation (Analytic Hierarchy Process) is documented in `../04_bqai/ahp_weights.py`.
