#!/usr/bin/env python3
import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CODEX_HOME = Path.home() / ".codex"

CORRECTION_RE = re.compile(
    r"(误解|不对|不是.*需求|卡住|失败|错了|下次不要|以后不要|反思|缺陷|问题)",
    re.IGNORECASE,
)


def load_registry(path: Path) -> list[dict]:
    text = path.read_text()
    skills: list[dict] = []
    current: dict | None = None
    current_key: str | None = None
    section: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line and not line.startswith(" "):
            section = line[:-1] if line.endswith(":") else None
            if current and section != "skills":
                skills.append(current)
                current = None
                current_key = None
            continue
        if section != "skills":
            continue
        if line.startswith("  - id: "):
            if current:
                skills.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
            current_key = None
            continue
        if current is None:
            continue

        stripped = line.strip()
        if stripped.startswith("category: "):
            current["category"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("status: "):
            current["status"] = stripped.split(":", 1)[1].strip()
        elif stripped in {"primary_when:", "do_not_use_when:", "codex_notes:"}:
            current_key = stripped[:-1]
            current.setdefault(current_key, [])
        elif current_key and stripped.startswith("- "):
            current[current_key].append(stripped[2:].strip())

    if current:
        skills.append(current)
    return skills


def iter_jsonl(path: Path):
    if not path.exists():
        return
    with path.open(errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def compile_skill_patterns(skills: list[dict]) -> dict[str, re.Pattern]:
    patterns = {}
    for skill in skills:
        skill_id = skill["id"]
        aliases = {skill_id, skill_id.replace("-", " ")}
        escaped = [re.escape(alias) for alias in aliases]
        patterns[skill_id] = re.compile(r"(?<![\w-])(" + "|".join(escaped) + r")(?![\w-])", re.IGNORECASE)
    return patterns


def compile_trigger_patterns(skills: list[dict]) -> dict[str, re.Pattern | None]:
    patterns = {}
    stop_words = {
        "the", "and", "or", "to", "a", "an", "is", "are", "when", "with",
        "work", "task", "user", "needs", "needed", "use", "using",
    }
    for skill in skills:
        phrases = []
        for item in skill.get("primary_when", []):
            words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}|[\u4e00-\u9fff]{2,}", item)
            for word in words:
                normalized = word.lower()
                if normalized not in stop_words:
                    phrases.append(word)
        if not phrases:
            patterns[skill["id"]] = None
            continue
        phrases = sorted(set(phrases), key=len, reverse=True)[:12]
        patterns[skill["id"]] = re.compile("|".join(re.escape(item) for item in phrases), re.IGNORECASE)
    return patterns


def unix_day(ts: int | float | None) -> str | None:
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(float(ts), timezone.utc).date().isoformat()
    except (TypeError, ValueError, OSError):
        return None


def parse_iso_day(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def add_signal(result: dict, skill_id: str, metric: str, day: str | None, source: str):
    result[skill_id][metric] += 1
    result[skill_id]["sources"].add(source)
    if day:
        latest = result[skill_id].get("latest_signal_day")
        if latest is None or day > latest:
            result[skill_id]["latest_signal_day"] = day


def analyze(codex_home: Path, registry: Path) -> dict:
    skills = load_registry(registry)
    by_id = {skill["id"]: skill for skill in skills}
    skill_patterns = compile_skill_patterns(skills)
    trigger_patterns = compile_trigger_patterns(skills)

    result = defaultdict(
        lambda: {
            "invocation_evidence_count": 0,
            "user_mention_count": 0,
            "trigger_opportunity_count": 0,
            "correction_count": 0,
            "repeat_repair_count": 0,
            "overlap_count": 0,
            "latest_signal_day": None,
            "sources": set(),
        }
    )

    for item in iter_jsonl(codex_home / "history.jsonl"):
        text = item.get("text", "")
        day = unix_day(item.get("ts"))
        matched_skills = []
        for skill_id, pattern in skill_patterns.items():
            if pattern.search(text):
                matched_skills.append(skill_id)
                add_signal(result, skill_id, "user_mention_count", day, "history")
        for skill_id, pattern in trigger_patterns.items():
            if pattern and pattern.search(text):
                matched_skills.append(skill_id)
                add_signal(result, skill_id, "trigger_opportunity_count", day, "history")
        if matched_skills and CORRECTION_RE.search(text):
            for skill_id in set(matched_skills):
                add_signal(result, skill_id, "correction_count", day, "history")

    for item in iter_jsonl(codex_home / "session_index.jsonl"):
        text = item.get("thread_name", "")
        day = parse_iso_day(item.get("updated_at"))
        for skill_id, pattern in skill_patterns.items():
            if pattern.search(text):
                add_signal(result, skill_id, "user_mention_count", day, "session_index")

    log_path = codex_home / "log" / "codex-tui.log"
    if log_path.exists():
        with log_path.open(errors="replace") as handle:
            for line in handle:
                if "SKILL.md" not in line and "/skills/" not in line:
                    continue
                day = line[:10] if re.match(r"\d{4}-\d{2}-\d{2}", line) else None
                for skill_id in by_id:
                    if f"/{skill_id}/SKILL.md" in line or f"/{skill_id}/" in line:
                        add_signal(result, skill_id, "invocation_evidence_count", day, "codex-tui.log")

    category_to_skills = defaultdict(list)
    for skill in skills:
        category_to_skills[skill.get("category", "uncategorized")].append(skill["id"])
    for skill_ids in category_to_skills.values():
        if len(skill_ids) <= 1:
            continue
        for skill_id in skill_ids:
            result[skill_id]["overlap_count"] = len(skill_ids) - 1

    today = datetime.now(timezone.utc).date()
    final = {}
    for skill in skills:
        skill_id = skill["id"]
        data = result[skill_id]
        latest = data["latest_signal_day"]
        staleness_days = None
        if latest:
            staleness_days = (today - datetime.fromisoformat(latest).date()).days
        usefulness = (
            2.0 * data["invocation_evidence_count"]
            + 1.0 * data["trigger_opportunity_count"]
            + 0.5 * data["user_mention_count"]
            - 1.5 * data["correction_count"]
            - 1.0 * data["repeat_repair_count"]
            - 0.5 * data["overlap_count"]
        )
        recommended_action = recommend_action(skill, data)
        final[skill_id] = {
            "status": skill.get("status"),
            "category": skill.get("category"),
            "metrics": {
                "invocation_evidence_count": data["invocation_evidence_count"],
                "user_mention_count": data["user_mention_count"],
                "trigger_opportunity_count": data["trigger_opportunity_count"],
                "correction_count": data["correction_count"],
                "repeat_repair_count": data["repeat_repair_count"],
                "overlap_count": data["overlap_count"],
                "staleness_days": staleness_days,
                "usefulness_score": usefulness,
            },
            "confidence": {
                "invocation_evidence_count": "direct",
                "user_mention_count": "direct",
                "trigger_opportunity_count": "inferred",
                "correction_count": "inferred",
                "repeat_repair_count": "inferred",
                "overlap_count": "inferred",
                "staleness_days": "derived",
                "usefulness_score": "derived",
            },
            "recommended_action": recommended_action,
            "latest_signal_day": latest,
            "evidence_sources": sorted(data["sources"]),
        }
    return {"registry": str(registry), "codex_home": str(codex_home), "skills": final}


def recommend_action(skill: dict, data: dict) -> str:
    status = skill.get("status", "")
    direct = data["invocation_evidence_count"]
    opportunities = data["trigger_opportunity_count"]
    corrections = data["correction_count"]
    overlaps = data["overlap_count"]

    if status in {"needs_codex_trim", "needs_codex_review", "needs_context_check"}:
        return "codex_adapt"
    if status == "draft":
        return "observe_more"
    if direct == 0 and opportunities == 0:
        return "archive_candidate"
    if direct == 0:
        return "observe_more"
    if corrections >= 3 and corrections >= max(2, opportunities * 0.2):
        return "trim"
    if overlaps >= 2 and direct + opportunities > 0:
        return "trim"
    return "keep"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze lightweight Codex skill usage signals.")
    parser.add_argument("--codex-home", type=Path, default=DEFAULT_CODEX_HOME)
    parser.add_argument("--registry", type=Path, default=ROOT / "registry" / "skills.yaml")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    output = analyze(args.codex_home.expanduser(), args.registry)
    print(json.dumps(output, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
