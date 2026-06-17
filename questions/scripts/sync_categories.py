#!/usr/bin/env python3
"""Sync question_registry → categories/*.md (read-only navigation layer)."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import fetch_all_questions, set_meta, utc_now  # noqa: E402
from paths import CATEGORIES_DIR, FILE_TO_CATEGORY, GENERATED_DIR  # noqa: E402

POISON_TEMPLATE = """<!-- ⛔ 禁止手动编辑！本文件由 sync_categories.py 从 question_registry 生成。
     改题请用: python questions/qcli.py edit ...
     上次同步: {sync_time} · manifest: {manifest_hash} -->
"""


def _yaml_list(items: list[str] | None) -> str | None:
    if not items:
        return None
    return yaml.dump(items, allow_unicode=True, default_flow_style=False).strip()


def render_question_block(q: dict) -> str:
    meta: dict = {
        "uid": q["uid"],
        "id": q["id"],
        "category": q["category"],
        "subcategory": q["subcategory"],
        "type": q["type"],
        "status": q["status"],
    }
    for key in ("interaction", "source", "depth", "order", "superseded_by", "deprecated_reason"):
        val = q.get(key if key != "order" else "order")
        if key == "order":
            val = q.get("order") or q.get("order_num")
        if val is not None and val != "":
            meta[key] = val
    if q.get("validation"):
        meta["validation"] = True
    if q.get("tags"):
        meta["tags"] = q["tags"]
    if q.get("prerequisites"):
        meta["prerequisites"] = q["prerequisites"]
    if q.get("related"):
        meta["related"] = q["related"]

    fm = yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False).strip()
    body = q["text"]
    if q.get("options"):
        for opt in q["options"]:
            body += f"\n- {opt['key']}. {opt['text']}"
    if q.get("scale") and q["scale"] not in body:
        body += f"\n{q['scale']}"
    return f"---\n{fm}\n---\n{body}\n\n"


def sync_categories() -> dict:
    CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)
    questions = fetch_all_questions()
    by_file: dict[str, list[dict]] = {fn: [] for fn in FILE_TO_CATEGORY}
    for q in questions:
        fn = q.get("source_file") or ""
        if fn not in by_file:
            for name, (slug, _) in FILE_TO_CATEGORY.items():
                if slug == q["category"]:
                    fn = name
                    break
        if fn in by_file:
            by_file[fn].append(q)

    sync_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    manifest: dict[str, str] = {}

    for filename, (slug, label) in FILE_TO_CATEGORY.items():
        items = by_file.get(filename, [])
        items.sort(key=lambda x: x["id"])
        subcats: dict[str, list[dict]] = {}
        for q in items:
            subcats.setdefault(q["subcategory"], []).append(q)

        content_parts = [
            f"# {label}",
            "",
            "> **只读导航层** — 由 `sync_categories.py` 自动生成。改题请用 `qcli edit`。",
            "",
        ]
        for subcat, qs in subcats.items():
            content_parts.append(f"## {subcat}")
            content_parts.append("")
            for q in qs:
                content_parts.append(render_question_block(q))

        body = "\n".join(content_parts).rstrip() + "\n"
        file_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()[:8]
        poison = POISON_TEMPLATE.format(sync_time=sync_time, manifest_hash=file_hash)
        final = poison + "\n" + body

        tmp = CATEGORIES_DIR / f".{filename}.tmp"
        dest = CATEGORIES_DIR / filename
        tmp.write_text(final, encoding="utf-8")
        tmp.replace(dest)
        manifest[filename] = hashlib.sha256(final.encode("utf-8")).hexdigest()

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    manifest_doc = {
        "synced_at": sync_time,
        "files": manifest,
    }
    (GENERATED_DIR / ".sync_manifest.json").write_text(
        json.dumps(manifest_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    set_meta("last_sync_at", utc_now())
    return manifest_doc


def main() -> int:
    doc = sync_categories()
    print(f"Synced {len(doc['files'])} category file(s) at {doc['synced_at']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
