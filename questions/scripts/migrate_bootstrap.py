#!/usr/bin/env python3
"""One-time bootstrap: categories/*.md or questions.json → question_registry.db."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "archive"))

import build_questions as bq  # noqa: E402
from db import (  # noqa: E402
    add_relation,
    get_connection,
    init_database,
    insert_question_record,
    load_registries,
    set_meta,
    utc_now,
)
from paths import CATEGORIES_DIR, GENERATED_DIR  # noqa: E402

MIGRATE_ERRORS = GENERATED_DIR / "migrate_errors.log"
MIGRATE_DIFF = GENERATED_DIR / "migrate_diff.log"


def log_error(source: str, qid: str, line: str, reason: str) -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    with MIGRATE_ERRORS.open("a", encoding="utf-8") as f:
        f.write(f"{source}\t{qid or '-'}\t{line}\t{reason}\n")


def clear_error_log() -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    MIGRATE_ERRORS.write_text("", encoding="utf-8")


def parse_categories_resilient() -> tuple[list[dict], int]:
    questions: list[dict] = []
    errors = 0
    for path in sorted(CATEGORIES_DIR.glob("*.md")):
        if path.name not in bq.FILE_TO_CATEGORY:
            continue
        slug, label = bq.FILE_TO_CATEGORY[path.name]
        content = path.read_text(encoding="utf-8")
        for match in bq.FM_BLOCK_PATTERN.finditer(content):
            meta = None
            try:
                meta = __import__("yaml").safe_load(match.group(1))
            except Exception as e:
                errors += 1
                log_error(path.name, "", str(match.start()), f"YAML parse: {e}")
                continue
            if not isinstance(meta, dict) or "id" not in meta:
                continue
            qid = str(meta.get("id", ""))
            try:
                base = bq.normalize_frontmatter(meta, slug, label, path.name)
                body = content[match.end():]
                nxt = bq.FM_BLOCK_PATTERN.search(body)
                body_text = body[: nxt.start()] if nxt else body
                body_lines = []
                for line in body_text.splitlines():
                    if line.startswith("## "):
                        break
                    body_lines.append(line)
                text, options, scale = bq.parse_options(body_lines)
                if not text:
                    raise ValueError("empty question text")
                base["text"] = text
                base["question"] = text
                base["options"] = options
                base["scale"] = scale
                questions.append(base)
            except Exception as e:
                errors += 1
                log_error(path.name, qid, str(match.start()), str(e))
    return questions, errors


def load_from_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for q in data:
        item = dict(q)
        item["question"] = item.get("text") or item.get("question")
        out.append(item)
    return out


def diff_json(path: Path, categories_qs: list[dict]) -> int:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        MIGRATE_DIFF.write_text("JSON file not found\n", encoding="utf-8")
        return 0
    json_qs = {q["id"]: q for q in load_from_json(path)}
    cat_qs = {q["id"]: q for q in categories_qs}
    lines = []
    for qid in sorted(set(json_qs) | set(cat_qs)):
        if qid not in json_qs:
            lines.append(f"ONLY_IN_CATEGORIES: {qid}")
        elif qid not in cat_qs:
            lines.append(f"ONLY_IN_JSON: {qid}")
        elif json_qs[qid].get("text") != cat_qs[qid].get("text"):
            lines.append(f"TEXT_DIFF: {qid}")
    MIGRATE_DIFF.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return len(lines)


def import_questions(questions: list[dict], *, source: str) -> tuple[int, int]:
    registries = load_registries()
    conn = get_connection()
    id_to_uid: dict[str, str] = {}
    imported = 0
    errors = 0
    try:
        conn.execute("DELETE FROM question_relations")
        conn.execute("DELETE FROM question_prerequisites")
        conn.execute("DELETE FROM question_tags")
        conn.execute("DELETE FROM questions")
        for q in questions:
            try:
                payload = {
                    "uid": q.get("uid"),
                    "id": q["id"],
                    "question": q.get("text") or q.get("question"),
                    "category": q["category"],
                    "subcategory": q["subcategory"],
                    "type": q["type"],
                    "interaction": q.get("interaction"),
                    "source": q.get("source"),
                    "status": q.get("status", "active"),
                    "depth": q.get("depth"),
                    "validation": q.get("validation", False),
                    "order": q.get("order"),
                    "deprecated_reason": q.get("deprecated_reason"),
                    "superseded_by": q.get("superseded_by"),
                    "tags": q.get("tags"),
                    "prerequisites": q.get("prerequisites"),
                    "options": q.get("options"),
                    "scale": q.get("scale"),
                }
                uid = insert_question_record(conn, payload, registries=registries)
                id_to_uid[q["id"]] = uid
                imported += 1
            except Exception as e:
                errors += 1
                log_error(source, q.get("id", ""), "-", str(e))
        for q in questions:
            related = q.get("related") or []
            src_uid = id_to_uid.get(q["id"])
            if not src_uid:
                continue
            for rid in related:
                tgt_uid = id_to_uid.get(rid)
                if tgt_uid:
                    add_relation(conn, q["id"], rid, "similar")
        conn.commit()
    finally:
        conn.close()
    set_meta("bootstrap_source", source)
    set_meta("bootstrap_at", utc_now())
    set_meta("question_count", str(imported))
    return imported, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap question_registry from legacy sources")
    parser.add_argument("--from-categories", action="store_true", default=True)
    parser.add_argument("--fallback-json", type=Path, help="Emergency import from questions.json")
    parser.add_argument("--diff-json", type=Path, help="Report differences only")
    parser.add_argument("--force", action="store_true", help="Recreate empty DB before import")
    args = parser.parse_args()

    if args.force:
        init_database(force=True)
    elif not Path(__import__("paths").DB_PATH).exists():
        init_database()

    clear_error_log()

    if args.diff_json:
        qs, _ = parse_categories_resilient()
        n = diff_json(args.diff_json, qs)
        print(f"Diff lines: {n} → {MIGRATE_DIFF}")
        return 0

    parse_errors = 0
    if args.fallback_json:
        questions = load_from_json(args.fallback_json)
        source = f"json:{args.fallback_json}"
    else:
        questions, parse_errors = parse_categories_resilient()
        source = "categories"
        if parse_errors:
            print(f"⚠️ 解析失败 {parse_errors} 条，请查看 {MIGRATE_ERRORS}", file=sys.stderr)

    imported, import_errors = import_questions(questions, source=source)
    total_errors = parse_errors + import_errors

    print(f"Imported {imported} question(s) from {source}")
    if total_errors:
        print(f"⚠️ 解析/导入失败 {total_errors} 条，见 {MIGRATE_ERRORS}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
