---
name: codex-token-budget
description: "Keep local Codex tasks within a token budget. Use for Codex work that may grow context or tool output: debugging slow or expensive sessions, analyzing token usage, planning large coding/refactoring/document/PDF/DOCX/PPTX/log/JSONL/XML tasks, deciding whether to resume or start fresh, or before running commands that can emit large outputs such as rg, find, git diff, unzip, qpdf, strings, tail, cat, jq, sqlite3, or long-running exec/write_stdin loops."
---

# Codex Token Budget

Use this skill as a guardrail before and during token-risky work. The goal is not
to avoid useful context; it is to stop accidental context growth from logs,
large documents, long transcripts, and repeated high-input turns.

## First Move

For local Codex token audits, run the bundled script before reading transcripts:

```bash
python3 /Users/xiaowenjie/.codex/skills/codex-token-budget/scripts/audit_codex_tokens.py --top 12 --sample 40
```

Only inspect a rollout body after the aggregate output identifies the specific
thread and the exact field needed.

## Risk Gate

Treat a task as high-risk when any item is true:

- It touches `.docx`, `.pptx`, `.pdf`, `.jsonl`, `.xml`, logs, rendered pages, or
  large generated reports.
- The user asks for "全面", "完整", "彻底", "深度", "全部", a broad review, or a
  multi-hour debugging pass.
- The task may need more than 10 tool calls or more than 3 large file reads.
- The current conversation is a resumed long session or already has many tool
  outputs.

For high-risk tasks, state a short budget plan before exploration: scope,
maximum files or commands, output limits, and when to stop or start a fresh
session.

## Hard Limits

- Prefer a new session over resuming when the prior task is complete, stale, or
  unrelated.
- If a session is already above 30M tokens, summarize and switch sessions before
  starting a new objective.
- If recent model calls are near 80k input tokens, avoid further broad reads and
  compress the working state into a short summary.
- Keep routine tool outputs below 2k tokens. Anything expected above 10k tokens
  must be replaced with counts, summaries, or sampled slices.
- Do not use high reasoning or the largest model for simple config checks,
  one-file fixes, or command-output inspection unless the user explicitly asks.

## Safer Command Patterns

Avoid commands that dump whole artifacts. Use aggregate-first commands instead.

- Replace broad `rg pattern huge-path` with `rg -c pattern huge-path`, then
  inspect only the highest-signal files with `sed -n` or `rg -n -m`.
- Replace full `find DIR -type f -print` with scoped `find DIR -maxdepth N -type f
| head` or `rg --files DIR | sed -n '1,80p'`.
- Replace raw `git diff` with `git diff --stat`, `git diff --name-only`, then
  targeted `git diff -- path`.
- Replace raw DOCX XML dumps with scripts that print paragraph/style counts and
  selected page/paragraph ranges.
- Replace `qpdf --json file.pdf` or `strings file.pdf` with page count, metadata,
  text extraction by page range, or a small grep sample.
- Replace log tailing of JSONL transcripts with `jq`/`sqlite3` counts and
  selected event fields.

## During Work

Keep a small ledger for high-risk tasks:

```text
budget: target <= X tool calls, <= Y files, no raw large dumps
seen: commands N, large outputs N, current risk low|medium|high
stop if: output >10k tokens, repeated failures, scope changes, or context grows
```

When a command unexpectedly returns huge output, do not continue reading around
it. Summarize what happened, switch to aggregate queries, and avoid repeating
similar commands.

## Evidence Standard

When explaining token waste, report concrete numbers:

- thread count and date span
- total tokens and largest threads
- model/reasoning distribution
- average and maximum per-call input tokens for sampled rollouts
- count of large tool outputs and representative command heads

Do not paste raw transcript content unless the user asks for exact excerpts.
