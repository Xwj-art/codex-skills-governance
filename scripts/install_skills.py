#!/usr/bin/env python3
import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = Path.home() / ".codex" / "skills"
DEFAULT_BACKUP = DEFAULT_TARGET / ".xwj-managed-backups"
DEFAULT_MANIFEST = DEFAULT_TARGET / ".xwj-managed-skills.json"


def skill_dirs(root: Path) -> list[Path]:
    return sorted(path for path in root.joinpath("skills").iterdir() if path.is_dir() and path.joinpath("SKILL.md").exists())


def describe_dst(dst: Path) -> str:
    if dst.is_symlink():
        return f"symlink -> {dst.readlink()}"
    if dst.exists():
        return "directory" if dst.is_dir() else "file"
    return "missing"


def path_present(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def backup_existing(dst: Path, backup_root: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root.mkdir(parents=True, exist_ok=True)
    backup = backup_root / f"{dst.name}-{stamp}"
    if backup.exists():
        raise RuntimeError(f"backup path already exists: {backup}")
    shutil.move(str(dst), str(backup))
    return backup


def main() -> int:
    parser = argparse.ArgumentParser(description="Install user-managed Codex skills from this repository.")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="Target skills directory")
    parser.add_argument("--skill", action="append", help="Install only this skill id; can be repeated")
    parser.add_argument("--apply", action="store_true", help="Actually copy files. Without this, only print the plan.")
    parser.add_argument("--replace", action="store_true", help="Replace existing target skill directories")
    parser.add_argument("--link", action="store_true", help="Install skills as symlinks to this repository instead of copying")
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_BACKUP, help="Where replaced directories are moved")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="Managed-skill manifest path")
    args = parser.parse_args()

    selected = set(args.skill or [])
    target = args.target.expanduser()
    backup_root = args.backup_dir.expanduser()
    manifest = args.manifest.expanduser()
    installed = []
    skipped = []
    manifest_entries = []

    for src in skill_dirs(ROOT):
        if selected and src.name not in selected:
            continue
        dst = target / src.name
        if path_present(dst) and not args.replace:
            skipped.append((src.name, describe_dst(dst)))
            continue
        installed.append(src.name)
        action = "link" if args.link else "copy"
        existing = describe_dst(dst)
        print(f"{action}: {src.relative_to(ROOT)} -> {dst} (existing: {existing})")
        if args.apply:
            if path_present(dst):
                if dst.is_symlink():
                    dst.unlink()
                elif args.replace:
                    backup = backup_existing(dst, backup_root)
                    print(f"backup: {dst.name} -> {backup}")
                else:
                    raise RuntimeError(f"target exists and --replace was not passed: {dst}")
            if args.link:
                dst.symlink_to(src, target_is_directory=True)
            else:
                shutil.copytree(src, dst)
        manifest_entries.append(
            {
                "name": src.name,
                "source": str(src),
                "target": str(dst),
                "mode": "symlink" if args.link else "copy",
            }
        )

    for name, reason in skipped:
        print(f"skip: {name} ({reason}; pass --replace to overwrite)")

    if not args.apply:
        print("dry-run only; pass --apply to copy/link files")
    else:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            json.dumps(
                {
                    "managed_by": "Xwj-art/codex-skills-governance",
                    "repository": str(ROOT),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                    "target": str(target),
                    "skills": manifest_entries,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
        print(f"manifest: {manifest}")

    print(f"planned={len(installed)} skipped={len(skipped)} target={target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
