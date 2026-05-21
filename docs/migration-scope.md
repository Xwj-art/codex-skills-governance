# Migration Scope

## Source Included Now

These are in scope because they are user-owned/user-maintained candidates and
are already visible to Codex or migrated from a user-owned GitHub repository.

### Codex-native or Codex-local skills

- `karpathy-codex`
- `execution-planning-contract`
- `codex-token-budget`
- `skill-usage-observer` (new draft in this governance workspace)
- `cost-aware-parallel-engineering`
- `parallel-task`
- `swarm-planner`
- `thesis-template-docx-fixer`
- `thesis-excellence-review` (migrated from `github.com/Xwj-art/thesis-excellence-review` by explicit user request)

### Agent skills exposed to Codex

- `growth`
- `habit-tracker`
- `learn`
- `qwen-asr`
- `qwen-image`

Note: `growth` still needs Codex-specific trimming before a public push.

## External Dependencies Tracked Only

These local skills may still be useful in Codex, but their source is not part of
the personal GitHub skill library unless ownership and redistribution are
confirmed:

- `academic-pptx`
- `marp-slides`
- `cli-creator`
- `figma-use`
- `figma-create-new-file`
- `figma-generate-design`
- `playwright-interactive`
- `screenshot`
- `coder`

## Excluded For Now

Do not touch the bulk of `~/.claude/skills`. Most of those skills were created
for Claude Code and have not been confirmed as Codex-used.

Specific exclusions:

- `tree-pipeline`: present in Claude skills and on GitHub, but not currently in
  the Codex available skill list. Migrate only after explicit Codex-use
  confirmation.
- `thesis-format-checker`: Python tool/library, not a skill. It belongs under a
  future `tools` registry if a Codex thesis skill calls it.
