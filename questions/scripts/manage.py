#!/usr/bin/env python3
"""Orchestration: sync pipeline and health checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import (  # noqa: E402
    fetch_all_questions,
    get_connection,
    load_registries,
    validate_options,
)
from paths import (  # noqa: E402
    GENERATED_DIR,
    IGNORE_EXTENSIONS,
    IMPORTS_PENDING,
    SOURCE_LIBRARY_DIR,
    CATEGORIES_DIR,
    DB_PATH,
)


def cmd_sync(args: argparse.Namespace) -> int:
    from ingest import ingest_pending
    from sync_categories import sync_categories
    from export_json import export_json
    from duplicate_scan import duplicate_scan

    if args.ingest:
        ingest_pending(sync=False, export=False)
    sync_categories()
    export_json()
    duplicate_scan()
    print("manage sync complete")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    issues: list[str] = []
    stale: list[str] = []
    warnings: list[str] = []

    if not DB_PATH.exists():
        issues.append(f"Missing database: {DB_PATH}")
    else:
        try:
            conn = get_connection(readonly=True)
            row = conn.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1").fetchone()
            conn.close()
            if not row:
                issues.append("schema_version empty")
        except Exception as e:
            issues.append(f"DB error: {e}")

        qs = fetch_all_questions()
        for q in qs:
            qid = q.get("id") or q.get("uid") or "?"
            for err in validate_options(q.get("options"), q.get("type", "open")):
                issues.append(f"{qid}: {err}")

        stats_path = GENERATED_DIR / "stats.json"
        if stats_path.exists():
            stats = json.loads(stats_path.read_text(encoding="utf-8"))
            db_total = len(qs)
            stats_total = stats.get("total_including_deprecated", stats.get("total"))
            if stats_total != db_total:
                stale.append(f"stats.json count mismatch: db={db_total} stats={stats_total}")

    manifest = GENERATED_DIR / ".sync_manifest.json"
    if manifest.exists() and CATEGORIES_DIR.exists():
        doc = json.loads(manifest.read_text(encoding="utf-8"))
        for fn, expected in doc.get("files", {}).items():
            p = CATEGORIES_DIR / fn
            if p.exists():
                actual = hashlib.sha256(p.read_text(encoding="utf-8").encode()).hexdigest()
                if actual != expected:
                    stale.append(f"categories/{fn} hash drift from manifest")

    if stale:
        stale.append("hint: run `python questions/scripts/manage.py sync`")

    if IMPORTS_PENDING.exists():
        pending = list(IMPORTS_PENDING.glob("*"))
        pending = [p for p in pending if p.is_file() and p.name != "README.md"]
        if pending:
            warnings.append(f"imports/pending has {len(pending)} file(s)")

    if SOURCE_LIBRARY_DIR.exists():
        for p in SOURCE_LIBRARY_DIR.rglob("*"):
            if p.is_file() and p.suffix.lower() in IGNORE_EXTENSIONS:
                print(f"[info] source_library attachment: {p.relative_to(SOURCE_LIBRARY_DIR)}")

    try:
        load_registries()
    except Exception as e:
        issues.append(f"registries yaml: {e}")

    for msg in stale:
        print(f"STALE: {msg}", file=sys.stderr)
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    for i in issues:
        print(f"ERROR: {i}", file=sys.stderr)
    if issues:
        return 1
    print("manage check OK")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Questions manage")
    sub = parser.add_subparsers(dest="command", required=True)
    p_sync = sub.add_parser("sync", help="ingest→sync_categories→export_json→duplicate_scan")
    p_sync.add_argument("--ingest", action="store_true", help="Process imports/pending first")
    p_sync.set_defaults(func=cmd_sync)
    p_check = sub.add_parser("check", help="Health check")
    p_check.set_defaults(func=cmd_check)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
