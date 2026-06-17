#!/usr/bin/env python3
"""Export question_registry → generated/questions.json, stats.json, registries.json."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import fetch_all_questions, load_registries, set_meta, utc_now  # noqa: E402
from paths import GENERATED_DIR  # noqa: E402


def compute_id_gaps_from_questions(questions: list[dict]) -> dict[str, list[int]]:
    import re
    pattern = re.compile(r"^Q-(REAL|EMO|DEC|STA|SELF|VAL|OTH)-(\d{3})$")
    by_prefix: dict[str, set[int]] = {}
    for q in questions:
        m = pattern.match(q["id"])
        if m:
            by_prefix.setdefault(m.group(1), set()).add(int(m.group(2)))
    gaps: dict[str, list[int]] = {}
    for prefix, nums in sorted(by_prefix.items()):
        if not nums:
            continue
        missing = [n for n in range(1, max(nums) + 1) if n not in nums]
        if missing:
            gaps[prefix] = missing
    return gaps


def build_stats(questions: list[dict], include_deprecated: bool = True) -> dict:
    active = [q for q in questions if q["status"] in ("active", "candidate")]
    pool = questions if include_deprecated else active
    return {
        "total": len(pool),
        "total_including_deprecated": len(questions),
        "by_category": dict(Counter(q["category"] for q in pool)),
        "by_subcategory": dict(
            Counter(f"{q['category']}:{q['subcategory']}" for q in pool),
        ),
        "by_source": dict(Counter(q["source"] or "(none)" for q in pool)),
        "by_status": dict(Counter(q["status"] for q in questions)),
        "by_type": dict(Counter(q["type"] for q in pool)),
        "missing_uid": [q["id"] for q in questions if not q.get("uid")],
        "id_gaps": compute_id_gaps_from_questions(questions),
        "with_prerequisites": sum(1 for q in pool if q.get("prerequisites")),
        "with_tags": sum(1 for q in pool if q.get("tags")),
    }


def export_registries_human_readable(registries: dict) -> None:
    lines = ["# Registries · human-readable snapshot", "", "> Auto-generated. Edit YAML only.", ""]
    for name in ("tags", "prerequisites"):
        raw = registries[name]["raw"]
        lines.append(f"## {name}")
        lines.append("")
        for entry in raw.get("entries") or []:
            if isinstance(entry, dict) and entry.get("id"):
                label = entry.get("label") or entry.get("name") or ""
                lines.append(f"- `{entry['id']}` — {label}")
        lines.append("")
    (GENERATED_DIR / "registries_human_readable.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8",
    )


def export_json(*, include_deprecated_in_export: bool = False) -> dict:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    questions = fetch_all_questions()
    export = questions if include_deprecated_in_export else [
        q for q in questions if q["status"] in ("active", "candidate")
    ]
    registries = load_registries()
    snapshot = {
        "prerequisites": registries["prerequisites"]["raw"],
        "tags": registries["tags"]["raw"],
    }
    stats = build_stats(questions)

    (GENERATED_DIR / "questions.json").write_text(
        json.dumps(export, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (GENERATED_DIR / "stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (GENERATED_DIR / "registries.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    export_registries_human_readable(registries)
    set_meta("last_export_at", utc_now())
    set_meta("question_count", str(len(questions)))
    return stats


def main() -> int:
    stats = export_json()
    print(f"Exported {stats['total']} active question(s) → {GENERATED_DIR / 'questions.json'}")
    print(f"Stats → {GENERATED_DIR / 'stats.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
