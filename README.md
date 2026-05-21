# Codex Skills Governance

This workspace stages the cleanup of user-owned or user-maintained skills that
are actually used with Codex. It is not a dump of every historical Claude Code
skill, and it is not a mirror of every locally installed skill.

## Scope Rule

Include a skill only when it satisfies at least one condition:

- It is user-authored or user-maintained.
- It is installed under `~/.codex/skills` and the user wants to manage it here.
- It is installed under `~/.agents/skills`, appears in Codex's available skill
  list, and the user confirms it belongs in the personal skill library.
- It is migrated from a repository owned by `Xwj-art`.

Do not organize, rewrite, or migrate skills that only exist under
`~/.claude/skills` until the user confirms Codex usage.

Do not commit third-party or bundled skill source just because it is installed
locally. Track those as external dependencies and conflict boundaries only.

## Goal

Prepare a single GitHub-managed source for Codex-ready skills:

- clear trigger boundaries,
- conflict resolution rules,
- Codex-specific adapters for Claude-era instructions,
- usage metrics for frequency, effectiveness, overlap, and staleness,
- an explicit migration status for each included skill.

Local install directories should eventually be generated from this repository
by sync or symlink scripts.

## Repository Layout

```text
skills/                 # user-owned/user-maintained skill source directories
registry/               # skill inventory, conflict boundaries, publish status
adapters/codex/         # Claude-era to Codex adaptation rules
docs/                   # migration and metrics documentation
scripts/                # validation, usage analysis, and install helpers
```

## Usage Observation

The draft `skill-usage-observer` skill measures how often skills are likely used
and where they appear ineffective or overlapping. It starts from lightweight
local evidence and avoids blocking on Codex sqlite databases.

Run the current analyzer from this directory:

```bash
python3 codex-skills-governance/scripts/analyze_skill_usage.py --pretty
```

The output is JSON so it can later feed a dashboard, report, or GitHub action.

## Local Install

Preview installing all migrated skills into `~/.codex/skills`:

```bash
python3 codex-skills-governance/scripts/install_skills.py
```

Apply the install only when ready:

```bash
python3 codex-skills-governance/scripts/install_skills.py --apply --replace
```

The install script copies from this repository to the target directory. It does
not push to GitHub and does not delete old repositories.
