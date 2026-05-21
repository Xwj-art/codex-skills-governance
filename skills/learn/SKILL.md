---
name: learn
description: Use when the user asks Codex to learn a project's conventions, extract reusable project rules, analyze codebase patterns, or update project-local Codex guidance such as AGENTS.md. For Codex, this skill does not write .claude/rules by default and does not use subagents unless the user explicitly asks for delegation or parallel agent work.
---

# Learn

Analyze a codebase to discover conventions that should guide future Codex work.
The output is evidence-based project guidance, not generic style advice.

## Codex Defaults

- Prefer updating or proposing changes to project-local `AGENTS.md`.
- Use `.codex/rules/` only when the project already uses that directory or the
  user explicitly asks for separate rule files.
- Do not write `.claude/rules/` unless the user explicitly asks for Claude Code
  compatibility.
- Do not spawn subagents unless the user explicitly asks for subagents,
  delegation, or parallel agent work.
- Never save rules automatically; present proposed rules first and wait for user
  approval before editing.

## When To Use

Use this skill when the user asks to:

- "learn from this project"
- "extract project rules"
- "analyze codebase conventions"
- "discover patterns"
- "update AGENTS.md based on the repo"
- make future Codex runs follow the current project's architecture or style

## Workflow

### 1. Establish Scope

Identify the project root and existing guidance:

```bash
ls -la AGENTS.md .codex/rules .claude/rules .cursorrules 2>/dev/null
```

Inspect lightweight project markers such as `package.json`, `pyproject.toml`,
`pom.xml`, `go.mod`, `composer.json`, `Makefile`, `README.md`, and test config.

### 2. Sample The Codebase

Use targeted searches instead of reading everything:

- directory layout and module boundaries
- entry points and dependency wiring
- tests and fixtures
- naming conventions
- error handling and logging
- data models, API envelopes, schemas, migrations, or DTO patterns
- existing scripts and validation commands

For large repos, inspect representative files per module and state sampling
limits.

### 3. Extract Candidate Rules

Each candidate rule must include:

- title
- scope
- evidence from at least two concrete files when possible
- the practical instruction Codex should follow
- counterexample or boundary condition
- confidence: `high`, `medium`, or `low`

Discard weak observations that are merely common language defaults or one-off
implementation details.

### 4. Present Before Writing

Show the top rules in this format:

```markdown
1. [RULE] <title> - <confidence>
   Evidence: <file>, <file>
   Instruction: <what Codex should do>
   Boundary: <when not to apply it>
```

Ask the user whether to save all, save selected rules, or keep the result as a
report only.

### 5. Persist Approved Rules

Default persistence target:

- If `AGENTS.md` exists, append or update a short "Project Rules" section.
- If `.codex/rules/` exists, write focused Markdown rule files there.
- If neither exists, ask before creating `AGENTS.md`.

Only use `.claude/rules/` when explicitly requested.

Before overwriting existing guidance, show the intended change and ask for
approval.

## Rule Quality Bar

Good rules are:

- specific to this project,
- backed by code evidence,
- short enough to stay useful in context,
- phrased as operational instructions,
- scoped so they do not overgeneralize.

Avoid:

- dumping long architecture summaries,
- writing obvious rules such as "write clean code",
- encoding personal guesses without evidence,
- mixing project rules with unrelated memories or global preferences.
