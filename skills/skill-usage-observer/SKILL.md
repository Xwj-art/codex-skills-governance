---
name: skill-usage-observer
description: Use when the user wants to measure Codex skill usage, compare skill effectiveness, find underused or overlapping skills, or decide which skills should be merged, trimmed, kept, archived, or rewritten for Codex.
---

# Skill Usage Observer

Use this skill to turn local Codex skill usage into measurable evidence before
changing the skill set.

## Scope

Measure only skills that are in the Codex governance registry or are explicitly
confirmed by the user as Codex-used.

Do not inventory all historical `~/.claude/skills` by default. Do not treat a
Claude-only skill as Codex-used just because it appears in an old note, GitHub
repository, or conversation title.

## Data Sources

Use lightweight local sources first:

- `~/.codex/history.jsonl` for user requests and corrections.
- `~/.codex/session_index.jsonl` for session-level titles.
- `~/.codex/log/codex-tui.log` for direct evidence such as opening `SKILL.md`
  files or running skill-related scripts.
- Governance files under the unified skill repository, especially
  `registry/skills.yaml`.

Treat sqlite databases under `~/.codex` as optional advanced sources only. They
can be large or locked while Codex is running, so never make them a blocking
dependency for a normal audit.

## Metrics

Report each metric with a confidence label: `direct`, `inferred`, or `manual`.

- `invocation_evidence_count`: direct evidence that a skill was loaded or its
  files/scripts were accessed.
- `user_mention_count`: user messages that explicitly name the skill.
- `trigger_opportunity_count`: user messages matching the skill's declared
  purpose or trigger keywords.
- `correction_count`: nearby user corrections after a likely skill use, such as
  "你误解", "不对", "卡住", "失败", "下次不要", or "不是这个需求".
- `repeat_repair_count`: repeated requests in the same topic that suggest the
  skill did not fully solve the problem.
- `overlap_count`: other skills sharing similar trigger terms or categories.
- `staleness_days`: days since the latest direct or inferred usage signal.
- `usefulness_score`: a derived score used for triage, not an absolute truth.

Suggested usefulness formula:

```text
usefulness_score =
  2.0 * invocation_evidence_count
  + 1.0 * trigger_opportunity_count
  + 0.5 * user_mention_count
  - 1.5 * correction_count
  - 1.0 * repeat_repair_count
  - 0.5 * overlap_count
```

## Triage

Use the metrics to classify skills:

- `keep`: direct usage evidence exists, correction rate is low, and the boundary
  is clear.
- `trim`: usage exists but the skill is too broad, too long, or overlaps with
  another skill.
- `split`: one skill owns multiple workflows with different success metrics.
- `merge`: two skills are triggered together and their boundary is artificial.
- `codex_adapt`: the skill contains Claude-era assumptions, especially mandatory
  multi-agent behavior.
- `observe_more`: only weak inferred evidence exists.
- `archive_candidate`: no direct usage evidence and no recent trigger
  opportunity.

## Workflow

1. Load `registry/skills.yaml` and the conflict boundary registry.
2. Collect direct evidence from lightweight local sources.
3. Compute metrics per skill and flag low-confidence fields.
4. Compare skills inside the same category before recommending changes.
5. Recommend a small action: keep, trim, split, merge, adapt, observe, or archive.
6. Do not rewrite a skill based on metrics alone; inspect the skill body before
   changing behavior.

## Output

Prefer a compact table with these columns:

- skill
- direct uses
- opportunities
- corrections
- overlaps
- staleness
- recommended action
- evidence note

For scripts, emit stable JSON so future dashboards or GitHub actions can reuse
the result.
