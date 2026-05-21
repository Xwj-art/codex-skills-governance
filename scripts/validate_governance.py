#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    ROOT / "README.md",
    ROOT / "docs" / "migration-scope.md",
    ROOT / "docs" / "ownership-scope.md",
    ROOT / "docs" / "metrics" / "skill-usage-metrics.md",
    ROOT / "registry" / "skills.yaml",
    ROOT / "registry" / "conflict-boundaries.yaml",
    ROOT / "registry" / "publish-readiness.yaml",
    ROOT / "adapters" / "codex" / "claude-legacy-rules.md",
    ROOT / "skills" / "skill-usage-observer" / "SKILL.md",
    ROOT / "scripts" / "analyze_skill_usage.py",
    ROOT / "scripts" / "install_skills.py",
]

missing = [str(path.relative_to(ROOT)) for path in required_files if not path.exists()]
if missing:
    raise SystemExit("missing required files: " + ", ".join(missing))

skills_text = (ROOT / "registry" / "skills.yaml").read_text()
boundaries_text = (ROOT / "registry" / "conflict-boundaries.yaml").read_text()

for forbidden in ["tree-pipeline"]:
    marker = f"excluded_until_confirmed:\n      - {forbidden}"
    if forbidden in skills_text:
        raise SystemExit(f"{forbidden} must not be in active skills.yaml")
    if marker not in boundaries_text:
        raise SystemExit(f"{forbidden} must appear only as excluded_until_confirmed")

if "thesis-format-checker" not in skills_text or "kind: python-tool" not in skills_text:
    raise SystemExit("thesis-format-checker must be classified as a python tool")

observer_skill = ROOT / "skills" / "skill-usage-observer" / "SKILL.md"
observer_text = observer_skill.read_text()
if "name: skill-usage-observer" not in observer_text:
    raise SystemExit("skill-usage-observer SKILL.md must declare its name")

for required_metric in [
    "invocation_evidence_count",
    "trigger_opportunity_count",
    "correction_count",
    "overlap_count",
    "staleness_days",
    "usefulness_score",
]:
    if required_metric not in observer_text:
        raise SystemExit(f"skill-usage-observer missing metric: {required_metric}")

if "skill-usage-observer" not in skills_text:
    raise SystemExit("skill-usage-observer must be registered in skills.yaml")

if "usage_metrics_or_effectiveness_review: skill-usage-observer" not in boundaries_text:
    raise SystemExit("skill-usage-observer boundary must be defined")

if "thesis-excellence-review" not in skills_text:
    raise SystemExit("thesis-excellence-review must be registered after migration")

if "full_thesis_excellence_review: thesis-excellence-review" not in boundaries_text:
    raise SystemExit("thesis-excellence-review boundary must be defined")

for skill_dir in ROOT.joinpath("skills").iterdir():
    if skill_dir.is_dir() and not skill_dir.joinpath("SKILL.md").exists():
        raise SystemExit(f"skill directory missing SKILL.md: {skill_dir.relative_to(ROOT)}")

publish_text = ROOT.joinpath("registry", "publish-readiness.yaml").read_text()
for external in [
    "academic-pptx",
    "marp-slides",
    "cli-creator",
    "figma-use",
    "figma-create-new-file",
    "figma-generate-design",
    "playwright-interactive",
    "screenshot",
    "coder",
]:
    if ROOT.joinpath("skills", external).exists():
        raise SystemExit(f"external skill source must not be committed: skills/{external}")
    if external not in publish_text:
        raise SystemExit(f"external skill must be tracked in publish-readiness.yaml: {external}")

print("governance files validated")
