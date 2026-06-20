#!/usr/bin/env python3
"""Export Agent-readable views → 03-generated-审计产物/01-agent-Agent视图/."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import fetch_all_questions, utc_now  # noqa: E402
from health_check import run_health_check  # noqa: E402
from paths import AGENT_VIEWS_DIR, BY_CATEGORY_DIR, FILE_TO_CATEGORY, GENERATED_DIR  # noqa: E402

AGENT_DIR = AGENT_VIEWS_DIR

CATEGORY_SLUGS = sorted({slug for slug, _ in FILE_TO_CATEGORY.values()})


def _compact_line(q: dict) -> str:
    text = (q.get("text") or q.get("question") or "").replace("\n", " ").strip()
    return f"{q['id']} · {q['subcategory']} · {text}"


def _index_entry(q: dict) -> dict:
    return {
        "id": q["id"],
        "uid": q.get("uid"),
        "category": q["category"],
        "subcategory": q["subcategory"],
        "type": q.get("type"),
        "source": q.get("source"),
        "status": q.get("status"),
        "interaction": q.get("interaction"),
    }


def _build_known_issues(stats: dict | None) -> str:
    lines = [
        "# Known issues · collect phase",
        "",
        "> Auto-generated. Fix in cleanup phase unless blocking ingest.",
        "",
    ]
    if not stats:
        lines.append("_stats.json not found_")
        return "\n".join(lines) + "\n"

    subcats = stats.get("by_subcategory") or {}
    education_keys = [k for k in subcats if "education" in k.lower() or "教育" in k]
    if len(education_keys) > 1:
        lines.extend([
            "## Subcategory naming",
            "",
            "Inconsistent education subcategory labels:",
            "",
        ])
        for k in education_keys:
            lines.append(f"- `{k}` ({subcats[k]} questions)")
        lines.append("")

    gaps = stats.get("id_gaps") or {}
    if gaps:
        lines.extend([
            "## ID gaps (normal)",
            "",
            "Skipped/rejected numbering — not errors:",
            "",
        ])
        for prefix, nums in sorted(gaps.items()):
            lines.append(f"- {prefix}: missing {nums}")
        lines.append("")

    lines.extend([
        "## Cleanup phase backlog",
        "",
        "- Scale near-duplicate clusters: no `similar` relations yet",
        "- Run `manage sync --with-duplicate-scan` after collection completes",
        "",
    ])
    return "\n".join(lines) + "\n"


def export_agent_views(*, batch_delta: dict | None = None) -> dict:
    """Write agent views; optionally update batch_delta.json."""
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    BY_CATEGORY_DIR.mkdir(parents=True, exist_ok=True)

    questions = fetch_all_questions()
    active = [q for q in questions if q["status"] in ("active", "candidate")]
    active.sort(key=lambda q: (q["category"], q["subcategory"], q["id"]))

    compact_lines = [
        "# Question bank · compact",
        "",
        f"> Active/candidate: {len(active)} · generated {utc_now()}",
        "",
        "Format: `id · subcategory · question`",
        "",
    ]
    for q in active:
        compact_lines.append(_compact_line(q))
    (AGENT_DIR / "bank_compact.md").write_text("\n".join(compact_lines) + "\n", encoding="utf-8")

    by_cat: dict[str, list[dict]] = defaultdict(list)
    for q in active:
        by_cat[q["category"]].append(q)

    for slug in CATEGORY_SLUGS:
        qs = by_cat.get(slug, [])
        cat_lines = [
            f"# {slug}",
            "",
            f"> {len(qs)} question(s)",
            "",
        ]
        for q in qs:
            cat_lines.append(_compact_line(q))
        (BY_CATEGORY_DIR / f"{slug}.md").write_text("\n".join(cat_lines) + "\n", encoding="utf-8")

    index = {
        "generated_at": utc_now(),
        "total_active": len(active),
        "questions": [_index_entry(q) for q in active],
    }
    (AGENT_DIR / "bank_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if batch_delta is not None:
        delta_doc = {
            "updated_at": utc_now(),
            **batch_delta,
        }
        (AGENT_DIR / "batch_delta.json").write_text(
            json.dumps(delta_doc, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        new_ids = batch_delta.get("new_ids") or []
        if new_ids:
            by_id = {q["id"]: q for q in active}
            delta_lines = [
                "# Batch delta · compact",
                "",
                f"> New questions: {len(new_ids)} · generated {utc_now()}",
                "",
                "Format: `id · subcategory · question`",
                "",
            ]
            for qid in new_ids:
                q = by_id.get(qid)
                if q:
                    delta_lines.append(_compact_line(q))
            (AGENT_DIR / "batch_delta_compact.md").write_text(
                "\n".join(delta_lines) + "\n",
                encoding="utf-8",
            )
    elif not (AGENT_DIR / "batch_delta.json").exists():
        placeholder = {
            "updated_at": utc_now(),
            "ingested_count": 0,
            "new_ids": [],
            "source_files": [],
            "note": "Run manage accept after jsonl is in 05-导入队列-Imports/01-pending-待入库/",
        }
        (AGENT_DIR / "batch_delta.json").write_text(
            json.dumps(placeholder, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    health = run_health_check()
    health["generated_at"] = utc_now()
    (GENERATED_DIR / "health.json").write_text(
        json.dumps(health, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    stats_path = GENERATED_DIR / "stats.json"
    stats = None
    if stats_path.exists():
        stats = json.loads(stats_path.read_text(encoding="utf-8"))
    (AGENT_DIR / "known_issues.md").write_text(_build_known_issues(stats), encoding="utf-8")

    return {
        "agent_dir": str(AGENT_DIR.relative_to(GENERATED_DIR.parent.parent)),
        "active_count": len(active),
        "health_ok": health["ok"],
    }


def main() -> int:
    result = export_agent_views()
    print(f"Agent views → {AGENT_DIR} ({result['active_count']} active)")
    return 0 if result["health_ok"] else 0


if __name__ == "__main__":
    sys.exit(main())
