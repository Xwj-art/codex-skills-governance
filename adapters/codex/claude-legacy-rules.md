# Codex Adapter Rules For Claude-Era Skills

Apply these rules only to skills confirmed as used from Codex.

## Subagents

Claude-era skills often say to use multiple agents by default. In Codex, this
must be adapted:

- Do not spawn subagents unless the user explicitly asks for subagents,
  delegation, or parallel agent work.
- Treat old "mandatory agent roles" as a local checklist unless explicit
  delegation is authorized.
- If delegation is authorized, use Codex `spawn_agent` rules and define
  disjoint ownership for code-editing workers.

## Paths

Replace Claude-only path assumptions:

- `~/.claude/skills` is not the Codex source of truth.
- Codex-ready skills should live in the future unified repository and be linked
  into `~/.codex/skills` or `~/.agents/skills`.
- Keep local private preferences and memories outside public GitHub repos.

## Tool References

Convert Claude-specific tool language into Codex-compatible instructions:

- Slash commands become explicit skill triggers or scripts.
- `Agent(...)` examples become optional delegation guidance, gated by user
  permission.
- Claude-specific role names become role checklists unless matching Codex
  subagent roles are available and explicitly authorized.

## Context Budget

For Codex, keep `SKILL.md` small:

- Put trigger conditions, boundaries, and the shortest workflow in `SKILL.md`.
- Move long examples, research notes, and provider details into `references/`.
- Put deterministic behavior into `scripts/`.

## Public Repo Hygiene

Before pushing a skill to GitHub:

- Remove personal paths, credentials, raw logs, and private SOP content.
- Mark provider-specific credentials as environment variable names only.
- Ensure tools and libraries are classified as tools, not skills.
