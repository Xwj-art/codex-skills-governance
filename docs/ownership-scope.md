# Ownership Scope

This repository is for skills the user owns or actively maintains for daily
Codex use. It is not a mirror of every skill installed locally.

## Publish Source Policy

Commit source code only for:

- skills authored by the user,
- skills migrated from the user's own GitHub repositories,
- skills the user explicitly chooses to maintain as personal Codex workflow
  skills.

Do not commit source code for:

- bundled OpenAI/system skills,
- third-party marketplace skills,
- skills that carry unclear redistribution rights,
- skills installed locally only as dependencies.

External skills may still be listed in the registry so their trigger boundaries
and conflicts are documented.

## Current Source-Included Skills

These directories currently live under `skills/` and are the candidates for the
new GitHub repository:

- `karpathy-codex`
- `execution-planning-contract`
- `codex-token-budget`
- `cost-aware-parallel-engineering`
- `parallel-task`
- `swarm-planner`
- `thesis-template-docx-fixer`
- `thesis-excellence-review`
- `skill-usage-observer`
- `qwen-asr`
- `qwen-image`
- `habit-tracker`
- `growth`
- `learn`

`growth` remains included as a Codex-adaptation candidate and should be trimmed
before a public push. `learn` has been adapted from Claude-specific rule output
to Codex-local project guidance.

## External Skills Tracked By Boundary Only

These are useful in local Codex but their source should not be included in this
repository unless ownership and redistribution are confirmed:

- `academic-pptx`
- `marp-slides`
- `cli-creator`
- `figma-use`
- `figma-create-new-file`
- `figma-generate-design`
- `playwright-interactive`
- `screenshot`
- `coder`
