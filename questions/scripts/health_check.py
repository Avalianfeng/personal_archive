#!/usr/bin/env python3
"""Structured health check for questions subsystem."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import fetch_all_questions, get_connection, load_registries, validate_options  # noqa: E402
from paths import (  # noqa: E402
    CATEGORIES_DIR,
    DB_PATH,
    GENERATED_DIR,
    IGNORE_EXTENSIONS,
    IMPORTS_PENDING,
    REPO_ROOT,
    SOURCE_LIBRARY_DIR,
)


def run_health_check() -> dict:
    """Return structured doctor result (no printing)."""
    issues: list[str] = []
    stale: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    if not DB_PATH.exists():
        issues.append(f"Missing database: {DB_PATH}")
    else:
        try:
            conn = get_connection(readonly=True)
            row = conn.execute(
                "SELECT version FROM schema_version ORDER BY version DESC LIMIT 1",
            ).fetchone()
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
                    stale.append(f"02-问题地图-Views/{fn} hash drift from manifest")

    if stale:
        stale.append("hint: run `python questions/scripts/manage.py sync`")

    if IMPORTS_PENDING.exists():
        pending = [
            p for p in IMPORTS_PENDING.glob("*")
            if p.is_file() and p.name != "README.md"
        ]
        if pending:
            warnings.append(f"{IMPORTS_PENDING.relative_to(REPO_ROOT).as_posix()} has {len(pending)} file(s)")

    if SOURCE_LIBRARY_DIR.exists():
        for p in SOURCE_LIBRARY_DIR.rglob("*"):
            if p.is_file() and p.suffix.lower() in IGNORE_EXTENSIONS:
                info.append(f"Library attachment: {p.relative_to(SOURCE_LIBRARY_DIR)}")

    try:
        load_registries()
    except Exception as e:
        issues.append(f"registries yaml: {e}")

    return {
        "ok": len(issues) == 0,
        "errors": issues,
        "stale": stale,
        "warnings": warnings,
        "info": info,
    }


def print_health_check(result: dict) -> int:
    for msg in result.get("stale") or []:
        print(f"STALE: {msg}", file=sys.stderr)
    for w in result.get("warnings") or []:
        print(f"WARNING: {w}", file=sys.stderr)
    for i in result.get("errors") or []:
        print(f"ERROR: {i}", file=sys.stderr)
    for line in result.get("info") or []:
        print(f"[info] {line}")
    if result.get("errors"):
        return 1
    print("manage check OK")
    return 0
