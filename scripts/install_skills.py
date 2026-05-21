#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = Path.home() / ".codex" / "skills"


def skill_dirs(root: Path) -> list[Path]:
    return sorted(path for path in root.joinpath("skills").iterdir() if path.is_dir() and path.joinpath("SKILL.md").exists())


def main() -> int:
    parser = argparse.ArgumentParser(description="Install unified Codex skills from this repository.")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="Target skills directory")
    parser.add_argument("--skill", action="append", help="Install only this skill id; can be repeated")
    parser.add_argument("--apply", action="store_true", help="Actually copy files. Without this, only print the plan.")
    parser.add_argument("--replace", action="store_true", help="Replace existing target skill directories")
    args = parser.parse_args()

    selected = set(args.skill or [])
    target = args.target.expanduser()
    installed = []
    skipped = []

    for src in skill_dirs(ROOT):
        if selected and src.name not in selected:
            continue
        dst = target / src.name
        if dst.exists() and not args.replace:
            skipped.append((src.name, "exists"))
            continue
        installed.append(src.name)
        action = "install" if not dst.exists() else "replace"
        print(f"{action}: {src.relative_to(ROOT)} -> {dst}")
        if args.apply:
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

    for name, reason in skipped:
        print(f"skip: {name} ({reason}; pass --replace to overwrite)")

    if not args.apply:
        print("dry-run only; pass --apply to copy files")

    print(f"planned={len(installed)} skipped={len(skipped)} target={target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
