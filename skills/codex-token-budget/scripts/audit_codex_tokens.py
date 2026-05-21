#!/usr/bin/env python3
"""Aggregate local Codex token usage without printing transcript bodies."""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
from collections import Counter
from pathlib import Path


DEFAULT_STATE_DB = Path.home() / ".codex" / "state_5.sqlite"


def connect(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def table(rows: list[list[object]], headers: list[str]) -> str:
    data = [[str(x) for x in row] for row in rows]
    widths = [len(h) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    fmt = "  ".join("{:<" + str(w) + "}" for w in widths)
    lines = [fmt.format(*headers), fmt.format(*["-" * w for w in widths])]
    lines.extend(fmt.format(*row) for row in data)
    return "\n".join(lines)


def query_rows(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
    return list(conn.execute(sql, params))


def summarize_rollout(path: str) -> dict[str, object]:
    stats: dict[str, object] = {
        "lines": 0,
        "file_mb": 0.0,
        "calls": 0,
        "avg_input": 0,
        "max_input": 0,
        "gt100k": 0,
        "compacts": 0,
        "tool_calls": 0,
        "big_outputs": 0,
        "huge_outputs": 0,
        "max_output": 0,
        "top_tools": "",
        "big_heads": "",
    }
    if not path or not os.path.exists(path):
        return stats

    stats["file_mb"] = round(os.path.getsize(path) / 1_000_000, 1)
    seen_totals: set[int] = set()
    inputs: list[int] = []
    calls: dict[str, tuple[str, str]] = {}
    tools: Counter[str] = Counter()
    big_heads: Counter[str] = Counter()

    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            stats["lines"] = int(stats["lines"]) + 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = obj.get("payload") or {}
            event_type = obj.get("type")

            if (
                event_type == "event_msg"
                and payload.get("type") == "token_count"
                and payload.get("info")
            ):
                info = payload["info"]
                total = (info.get("total_token_usage") or {}).get("total_tokens")
                if total is not None and total not in seen_totals:
                    seen_totals.add(total)
                    last = info.get("last_token_usage") or {}
                    inputs.append(int(last.get("input_tokens") or 0))
            elif event_type == "event_msg" and payload.get("type") == "context_compacted":
                stats["compacts"] = int(stats["compacts"]) + 1
            elif event_type == "response_item" and payload.get("type") == "function_call":
                name = payload.get("name") or "?"
                tools[name] += 1
                stats["tool_calls"] = int(stats["tool_calls"]) + 1
                cmd = ""
                args = payload.get("arguments") or ""
                try:
                    parsed = json.loads(args) if isinstance(args, str) else args
                    if isinstance(parsed, dict):
                        cmd = parsed.get("cmd") or parsed.get("path") or ""
                except Exception:
                    cmd = ""
                calls[payload.get("call_id")] = (name, cmd)
            elif event_type == "response_item" and payload.get("type") == "function_call_output":
                output = payload.get("output") or ""
                if not isinstance(output, str):
                    output = json.dumps(output, ensure_ascii=False)[:1000]
                match = re.search(r"Original token count: (\d+)", output)
                if not match:
                    continue
                count = int(match.group(1))
                stats["max_output"] = max(int(stats["max_output"]), count)
                if count >= 10_000:
                    stats["big_outputs"] = int(stats["big_outputs"]) + 1
                    _, cmd = calls.get(payload.get("call_id"), ("?", ""))
                    head = (cmd.split() or ["?"])[0]
                    big_heads[head] += 1
                if count >= 50_000:
                    stats["huge_outputs"] = int(stats["huge_outputs"]) + 1

    stats["calls"] = len(inputs)
    if inputs:
        stats["avg_input"] = int(sum(inputs) / len(inputs))
        stats["max_input"] = max(inputs)
        stats["gt100k"] = sum(1 for value in inputs if value >= 100_000)
    stats["top_tools"] = ",".join(f"{k}:{v}" for k, v in tools.most_common(3))
    stats["big_heads"] = ",".join(f"{k}:{v}" for k, v in big_heads.most_common(5))
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DEFAULT_STATE_DB), help="Path to state_5.sqlite")
    parser.add_argument("--top", type=int, default=12, help="Top threads to list")
    parser.add_argument("--sample", type=int, default=40, help="High-token rollouts to inspect")
    parser.add_argument("--threshold", type=int, default=10_000_000, help="High-token threshold")
    args = parser.parse_args()

    db = Path(args.db).expanduser()
    if not db.exists():
        raise SystemExit(f"missing Codex state DB: {db}")

    conn = connect(db)
    overview = query_rows(
        conn,
        """
        select count(*) as n,
               min(datetime(created_at,'unixepoch','localtime')) as first_seen,
               max(datetime(updated_at,'unixepoch','localtime')) as last_seen,
               sum(tokens_used) as sum_tokens,
               max(tokens_used) as max_tokens,
               round(avg(tokens_used),0) as avg_tokens
        from threads where tokens_used > 0
        """,
    )[0]
    print("Overview")
    print(
        table(
            [[overview["n"], overview["first_seen"], overview["last_seen"], overview["sum_tokens"], overview["max_tokens"], overview["avg_tokens"]]],
            ["threads", "first_seen", "last_seen", "sum_tokens", "max_tokens", "avg_tokens"],
        )
    )

    print("\nToken Buckets")
    bucket_rows = query_rows(
        conn,
        """
        select case
                 when tokens_used < 100000 then '<100k'
                 when tokens_used < 1000000 then '100k-1M'
                 when tokens_used < 10000000 then '1M-10M'
                 when tokens_used < 50000000 then '10M-50M'
                 when tokens_used < 100000000 then '50M-100M'
                 else '100M+'
               end as bucket,
               count(*) as n,
               sum(tokens_used) as sum_tokens
        from threads
        where tokens_used > 0
        group by bucket
        order by min(tokens_used)
        """,
    )
    print(table([[r["bucket"], r["n"], r["sum_tokens"]] for r in bucket_rows], ["bucket", "threads", "tokens"]))

    print("\nTop Model/Effort")
    model_rows = query_rows(
        conn,
        """
        select model, reasoning_effort, count(*) as n, sum(tokens_used) as sum_tokens,
               round(avg(tokens_used),0) as avg_tokens, max(tokens_used) as max_tokens
        from threads
        where tokens_used > 0
        group by model, reasoning_effort
        order by sum_tokens desc
        limit 10
        """,
    )
    print(
        table(
            [[r["model"], r["reasoning_effort"], r["n"], r["sum_tokens"], r["avg_tokens"], r["max_tokens"]] for r in model_rows],
            ["model", "effort", "threads", "tokens", "avg", "max"],
        )
    )

    print("\nTop Threads")
    top_rows = query_rows(
        conn,
        """
        select id, tokens_used, model, reasoning_effort, cwd, first_user_message, rollout_path
        from threads
        where tokens_used > 0
        order by tokens_used desc
        limit ?
        """,
        (args.top,),
    )
    print(
        table(
            [
                [
                    r["id"][:8],
                    f"{r['tokens_used'] / 1_000_000:.1f}M",
                    r["model"],
                    r["reasoning_effort"],
                    Path(r["cwd"]).name or r["cwd"],
                    (r["first_user_message"] or "").replace("\n", " ")[:44],
                ]
                for r in top_rows
            ],
            ["id", "tokens", "model", "effort", "cwd", "first_message"],
        )
    )

    print("\nHigh-Token Rollout Sample")
    sample_rows = query_rows(
        conn,
        """
        select id, tokens_used, rollout_path, first_user_message
        from threads
        where tokens_used >= ?
        order by tokens_used desc
        limit ?
        """,
        (args.threshold, args.sample),
    )
    aggregate = Counter()
    rows: list[list[object]] = []
    for r in sample_rows:
        stats = summarize_rollout(r["rollout_path"])
        if int(stats["avg_input"]) >= 100_000:
            aggregate["avg_input>=100k"] += 1
        if int(stats["max_input"]) >= 200_000:
            aggregate["max_input>=200k"] += 1
        if int(stats["big_outputs"]):
            aggregate["has_output>=10k"] += 1
        if int(stats["huge_outputs"]):
            aggregate["has_output>=50k"] += 1
        if int(stats["compacts"]):
            aggregate["has_compaction"] += 1
        rows.append(
            [
                r["id"][:8],
                f"{r['tokens_used'] / 1_000_000:.1f}M",
                stats["calls"],
                stats["avg_input"],
                stats["max_input"],
                stats["big_outputs"],
                stats["huge_outputs"],
                stats["top_tools"],
                stats["big_heads"],
            ]
        )
    print(table(rows[: min(args.top, len(rows))], ["id", "tokens", "calls", "avg_in", "max_in", "big", "huge", "tools", "big_heads"]))
    print("\nSample Flags")
    for key, value in aggregate.most_common():
        print(f"{key}: {value}/{len(sample_rows)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
