# Skill Usage Metrics

This document defines the first measurable layer for managing Codex skills.
The goal is not to prove perfect causality; it is to make skill cleanup less
subjective.

## Evidence Levels

- `direct`: Codex logs show a skill file, skill script, or explicit invocation
  marker.
- `inferred`: user text, session title, or trigger terms suggest a skill should
  have applied.
- `manual`: a human review confirms the skill was used or was responsible for
  the outcome.

Direct evidence should carry more weight than inferred evidence. Manual evidence
should include a short note and date when it is added to the registry.

## Core Metrics

| metric                      | meaning                                      | preferred source                        |
| --------------------------- | -------------------------------------------- | --------------------------------------- |
| `invocation_evidence_count` | Skill was probably loaded or used            | `codex-tui.log`, `SKILL.md` path access |
| `user_mention_count`        | User explicitly named the skill              | `history.jsonl`, `session_index.jsonl`  |
| `trigger_opportunity_count` | User request matched declared triggers       | registry keywords, descriptions         |
| `correction_count`          | Nearby user correction after likely use      | `history.jsonl`                         |
| `repeat_repair_count`       | Repeated same-topic repairs after use        | session history                         |
| `overlap_count`             | Similar trigger/category conflict            | `registry/conflict-boundaries.yaml`     |
| `staleness_days`            | Days since the latest signal                 | all lightweight sources                 |
| `usefulness_score`          | Triage score for keep/trim/archive decisions | derived                                 |

## Initial Decision Rules

- Keep a skill when it has direct evidence and few corrections.
- Trim a skill when usage exists but the skill has broad triggers, long
  instruction bodies, or frequent overlap.
- Adapt a skill when the content assumes Claude Code behavior that conflicts
  with Codex, especially mandatory subagents.
- Observe more when only inferred evidence exists.
- Treat archive decisions as reversible until the unified repository has install
  and sync scripts.

## Privacy And Safety

The analyzer should not print raw conversation text by default. It should report
counts, timestamps, session ids, and short evidence categories. Raw excerpts are
allowed only when explicitly requested for manual review.
