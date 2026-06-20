#!/usr/bin/env python3
"""Ingest jsonl/json from 05-导入队列-Imports/01-pending-待入库|external → 04-存储层-Store."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import (  # noqa: E402
    append_audit,
    get_connection,
    insert_question_record,
    load_registries,
    post_write_hooks,
    prepare_ingest_record,
    validate_ingest_path,
)
from paths import IMPORTS_FAILED, IMPORTS_PENDING, IMPORTS_PROCESSED, IMPORTS_EXTERNAL  # noqa: E402


def _ts_suffix() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_jsonl_content(text: str) -> tuple[dict[str, object], list[tuple[int, dict]]]:
    """Return batch context and question records as (line_no, raw_dict) pairs."""
    text = text.strip()
    if not text:
        return {}, []
    batch_ctx: dict[str, object] = {}
    records: list[tuple[int, dict]] = []
    for i, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"line {i}: {e}") from e
        if not isinstance(obj, dict):
            raise ValueError(f"line {i}: expected JSON object")
        if obj.get("_meta") is True:
            for key, value in obj.items():
                if key != "_meta":
                    batch_ctx[key] = value
            continue
        records.append((i, obj))
    return batch_ctx, records


def parse_lines(path: Path) -> list[dict]:
    """Legacy helper: raw question dicts only (excludes _meta lines)."""
    _, records = parse_jsonl_content(path.read_text(encoding="utf-8"))
    return [rec for _, rec in records]


def validate_jsonl_file(path: Path) -> list[str]:
    """Dry-run validation for one jsonl/json file."""
    validate_ingest_path(path)
    registries = load_registries()
    try:
        text = path.read_text(encoding="utf-8").strip()
        if path.suffix.lower() == ".json":
            data = json.loads(text)
            items = data if isinstance(data, list) else [data]
            batch_ctx: dict[str, object] = {}
            records = [(i, rec) for i, rec in enumerate(items, 1) if isinstance(rec, dict)]
        else:
            batch_ctx, records = parse_jsonl_content(text)
    except Exception as e:
        return [str(e)]
    if not records:
        return ["empty file (no question records)"]
    errors: list[str] = []
    ctx = dict(batch_ctx)
    for line_no, rec in records:
        if rec.get("_meta") is True:
            continue
        _, rec_errors = prepare_ingest_record(rec, ctx, registries=registries, line=line_no)
        errors.extend(rec_errors)
    return errors


def iter_ingest_paths() -> list[Path]:
    paths: list[Path] = []
    for directory in (IMPORTS_PENDING, IMPORTS_EXTERNAL):
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*")):
            if path.is_file() and path.suffix.lower() in {".jsonl", ".json"}:
                if path.name.endswith(".rejected.jsonl"):
                    continue
                paths.append(path)
    return paths


def validate_pending() -> list[str]:
    errors: list[str] = []
    for path in iter_ingest_paths():
        file_errors = validate_jsonl_file(path)
        for err in file_errors:
            errors.append(f"{path.name}: {err}")
    return errors


def archive(path: Path, dest_dir: Path, *, failed: bool, error: str | None = None) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    if failed:
        target = dest_dir / path.name
        path.replace(target)
        if error:
            (dest_dir / f"{path.name}.error.log").write_text(error + "\n", encoding="utf-8")
    else:
        stem = path.stem
        suffix = path.suffix
        target = dest_dir / f"{stem}_ingested_{_ts_suffix()}{suffix}"
        path.replace(target)


def _load_file_records(path: Path) -> tuple[dict[str, object], list[tuple[int, dict]]]:
    text = path.read_text(encoding="utf-8").strip()
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        items = data if isinstance(data, list) else [data]
        batch_ctx: dict[str, object] = {}
        records = [(i, rec) for i, rec in enumerate(items, 1) if isinstance(rec, dict)]
        return batch_ctx, records
    return parse_jsonl_content(text)


def ingest_file(
    path: Path,
    *,
    sync: bool = False,
    export: bool = False,
    dry_run: bool = False,
) -> int:
    validate_ingest_path(path)
    file_errors = validate_jsonl_file(path)
    if file_errors:
        msg = "; ".join(file_errors)
        if not dry_run:
            archive(path, IMPORTS_FAILED, failed=True, error=msg)
        raise ValueError(msg)

    batch_ctx, records = _load_file_records(path)
    if dry_run:
        print(f"OK: {len(records)} record(s) in {path.name}")
        return len(records)

    registries = load_registries()
    conn = get_connection()
    count = 0
    ctx = dict(batch_ctx)
    try:
        for line_no, rec in records:
            prepared, prep_errors = prepare_ingest_record(
                rec, ctx, registries=registries, line=line_no,
            )
            if prep_errors:
                raise ValueError("; ".join(prep_errors))
            if prepared is None:
                continue
            insert_question_record(conn, prepared, registries=registries)
            count += 1
        conn.commit()
    except Exception as e:
        conn.rollback()
        archive(path, IMPORTS_FAILED, failed=True, error=str(e))
        raise
    finally:
        conn.close()

    append_audit("ingest", f"file:{path.name}", None, {"count": count}, {"records": count})
    archive(path, IMPORTS_PROCESSED, failed=False)
    if sync or export:
        post_write_hooks(sync=sync, export=export)
    return count


def ingest_pending(*, sync: bool = False, export: bool = False, dry_run: bool = False) -> int:
    total = 0
    for path in iter_ingest_paths():
        total += ingest_file(path, sync=sync, export=export, dry_run=dry_run)
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest pending jsonl/json files")
    parser.add_argument("--file", type=Path, help="Single file to ingest")
    parser.add_argument("--stdin", action="store_true", help="Read jsonl from stdin")
    parser.add_argument("--dry-run", action="store_true", help="Validate only; do not write DB")
    parser.add_argument("--sync", action="store_true", help="Run sync_categories after ingest")
    parser.add_argument("--export", action="store_true", help="Run export_json after ingest")
    parser.add_argument(
        "--no-sync",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()

    sync = args.sync and not args.dry_run
    export = (args.export or args.sync) and not args.dry_run

    if args.dry_run and not args.file and not args.stdin:
        errors = validate_pending()
        if errors:
            for err in errors:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        n = sum(len(parse_lines(p)) for p in iter_ingest_paths())
        print(f"OK: {n} record(s) in {len(iter_ingest_paths())} file(s)")
        return 0

    if args.stdin:
        data = sys.stdin.read()
        tmp = IMPORTS_PENDING / f"_stdin_{_ts_suffix()}.jsonl"
        IMPORTS_PENDING.mkdir(parents=True, exist_ok=True)
        tmp.write_text(data, encoding="utf-8")
        n = ingest_file(tmp, sync=sync, export=export, dry_run=args.dry_run)
        label = "Validated" if args.dry_run else "Ingested"
        print(f"{label} {n} record(s) from stdin")
        return 0

    if args.file:
        n = ingest_file(args.file, sync=sync, export=export, dry_run=args.dry_run)
        label = "Validated" if args.dry_run else "Ingested"
        print(f"{label} {n} record(s) from {args.file}")
        return 0

    n = ingest_pending(sync=sync, export=export, dry_run=args.dry_run)
    label = "Validated" if args.dry_run else "Ingested"
    print(f"{label} {n} record(s) from pending/external queues")
    return 0


if __name__ == "__main__":
    sys.exit(main())
