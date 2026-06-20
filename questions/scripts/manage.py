#!/usr/bin/env python3
"""Orchestration: sync pipeline and health checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import fetch_all_questions  # noqa: E402
from health_check import print_health_check, run_health_check  # noqa: E402
from paths import AGENT_VIEWS_DIR, GENERATED_DIR, IMPORTS_PENDING  # noqa: E402


def _run_sync_pipeline(*, with_duplicate_scan: bool = False, batch_delta: dict | None = None) -> dict:
    from export_agent_views import export_agent_views
    from export_json import export_json
    from sync_categories import sync_categories

    sync_categories()
    export_json()
    agent_result = export_agent_views(batch_delta=batch_delta)

    if with_duplicate_scan:
        from duplicate_scan import duplicate_scan
        duplicate_scan()

    return agent_result


def cmd_sync(args: argparse.Namespace) -> int:
    if args.ingest:
        from ingest import ingest_pending
        ingest_pending(sync=False, export=False)

    _run_sync_pipeline(with_duplicate_scan=args.with_duplicate_scan)

    if args.json:
        click_json = {
            "ok": True,
            "command": "sync",
            "with_duplicate_scan": args.with_duplicate_scan,
            "agent_views": str(AGENT_VIEWS_DIR.relative_to(GENERATED_DIR.parent.parent)).replace("\\", "/"),
        }
        print(json.dumps(click_json, ensure_ascii=False, indent=2))
    else:
        print("manage sync complete")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    health_path = GENERATED_DIR / "health.json"
    if health_path.exists() and getattr(args, "from_cache", False):
        result = json.loads(health_path.read_text(encoding="utf-8"))
    else:
        result = run_health_check()
        result["generated_at"] = result.get("generated_at") or __import__("db").utc_now()
        GENERATED_DIR.mkdir(parents=True, exist_ok=True)
        health_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if getattr(args, "json", False):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 1
    return print_health_check(result)


def cmd_accept(args: argparse.Namespace) -> int:
    """Batch acceptance: validate → ingest → sync → doctor."""
    from ingest import ingest_pending, validate_pending

    source_files: list[str] = []
    if not args.skip_validate:
        errors = validate_pending()
        if errors:
            for err in errors:
                print(f"ERROR: {err}", file=sys.stderr)
            print("Fix jsonl in 05-导入队列-Imports/01-pending-待入库/ then retry.", file=sys.stderr)
            if args.json:
                print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
            return 1
        paths = [
            p for p in IMPORTS_PENDING.glob("*")
            if p.is_file() and p.suffix.lower() in {".jsonl", ".json"}
        ] if IMPORTS_PENDING.exists() else []
        if not paths:
            msg = "Nothing to ingest in 05-导入队列-Imports/01-pending-待入库/"
            print(msg, file=sys.stderr)
            if args.json:
                print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False, indent=2))
            return 1
        source_files = [p.name for p in paths]
        if not args.json:
            print(f"Validated {len(paths)} file(s)")

    before_ids = {q["id"] for q in fetch_all_questions()}
    n = ingest_pending(sync=False, export=False)
    after_ids = {q["id"] for q in fetch_all_questions()}
    new_ids = sorted(after_ids - before_ids)

    batch_delta = {
        "ingested_count": n,
        "new_ids": new_ids,
        "source_files": source_files,
    }

    _run_sync_pipeline(
        with_duplicate_scan=args.with_duplicate_scan,
        batch_delta=batch_delta,
    )

    health = run_health_check()
    health_path = GENERATED_DIR / "health.json"
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    health_path.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not args.json:
        print(f"Ingested {n} record(s)")
        print("Synced categories + exported json + agent views")

    rc = print_health_check(health) if not args.json else (0 if health["ok"] else 1)

    if args.json:
        payload = {
            "ok": health["ok"],
            "ingested": n,
            "new_ids": new_ids,
            "source_files": source_files,
            "health": health,
            "agent_views": str(AGENT_VIEWS_DIR.relative_to(GENERATED_DIR.parent.parent)).replace("\\", "/"),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return rc

    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description="Questions manage")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sync = sub.add_parser("sync", help="sync_categories→export_json→export_agent_views")
    p_sync.add_argument("--ingest", action="store_true", help="Process 05-导入队列-Imports/01-pending-待入库 first")
    p_sync.add_argument(
        "--with-duplicate-scan",
        action="store_true",
        help="Also run duplicate_scan (cleanup phase)",
    )
    p_sync.add_argument("--json", action="store_true", help="JSON stdout")
    p_sync.set_defaults(func=cmd_sync)

    p_check = sub.add_parser("check", help="Health check")
    p_check.add_argument("--json", action="store_true", help="JSON stdout")
    p_check.set_defaults(func=cmd_check)

    p_accept = sub.add_parser(
        "accept",
        help="Batch acceptance: validate pending jsonl → ingest → sync → doctor",
    )
    p_accept.add_argument("--skip-validate", action="store_true")
    p_accept.add_argument("--with-duplicate-scan", action="store_true")
    p_accept.add_argument("--json", action="store_true", help="JSON stdout")
    p_accept.set_defaults(func=cmd_accept)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
