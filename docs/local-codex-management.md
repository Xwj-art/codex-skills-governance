# Local Codex Skill Management

Codex discovers normal skill entries from top-level directories under
`~/.codex/skills`. To keep user-owned skills centralized without breaking that
discovery model, this repository uses symlinks:

```text
~/.codex/skills/karpathy-codex -> <repo>/skills/karpathy-codex
~/.codex/skills/learn          -> <repo>/skills/learn
```

The Git repository remains the source of truth. `~/.codex/skills` becomes the
runtime view Codex reads.

## Separation Rule

- User-owned / user-maintained skills: source lives in this repository and is
  symlinked into `~/.codex/skills`.
- System skills: stay under `~/.codex/skills/.system`.
- Bundled/plugin skills: stay under plugin cache directories.
- Third-party skills: may stay installed locally, but source is not copied here
  unless ownership and redistribution are confirmed.
- Agent-surface skills in `~/.agents/skills`: migrate here only when the user
  chooses to maintain them personally.

## Install Preview

From the repository root:

```bash
python3 scripts/install_skills.py --link
```

## Apply Symlink Management

```bash
python3 scripts/install_skills.py --link --apply --replace
```

Existing local directories with the same skill name are moved to:

```text
~/.codex/skills/.xwj-managed-backups/
```

The script writes:

```text
~/.codex/skills/.xwj-managed-skills.json
```

Use that manifest to audit which runtime skills are controlled by this
repository.
