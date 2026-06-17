#!/usr/bin/env python3
"""Ingest jsonl/json from imports/pending|external → question_registry."""

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
    validate_ingest_path,
)
from paths import IMPORTS_FAILED, IMPORTS_PENDING, IMPORTS_PROCESSED, IMPORTS_EXTERNAL  # noqa: E402


def _ts_suffix() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_lines(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    items = []
    for i, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                items.append(obj)
        except json.JSONDecodeError as e:
            raise ValueError(f"line {i}: {e}") from e
    return items


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


def ingest_file(path: Path, *, sync: bool = True, export: bool = True) -> int:
    validate_ingest_path(path)
    registries = load_registries()
    try:
        records = parse_lines(path)
    except Exception as e:
        archive(path, IMPORTS_FAILED, failed=True, error=str(e))
        raise
    if not records:
        archive(path, IMPORTS_FAILED, failed=True, error="empty file")
        raise ValueError("empty ingest file")

    conn = get_connection()
    count = 0
    try:
        for i, rec in enumerate(records, 1):
            if "question" not in rec and "text" not in rec:
                raise ValueError(f"record {i}: missing question/text")
            insert_question_record(conn, rec, registries=registries)
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


def ingest_pending(*, sync: bool = True, export: bool = True) -> int:
    total = 0
    for directory in (IMPORTS_PENDING, IMPORTS_EXTERNAL):
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*")):
            if path.suffix.lower() not in {".jsonl", ".json"}:
                continue
            total += ingest_file(path, sync=sync, export=export)
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest pending jsonl/json files")
    parser.add_argument("--file", type=Path, help="Single file to ingest")
    parser.add_argument("--stdin", action="store_true", help="Read jsonl from stdin")
    parser.add_argument("--no-sync", action="store_true")
    parser.add_argument("--no-export", action="store_true")
    args = parser.parse_args()

    sync = not args.no_sync
    export = not args.no_export

    if args.stdin:
        data = sys.stdin.read()
        tmp = IMPORTS_PENDING / f"_stdin_{_ts_suffix()}.jsonl"
        IMPORTS_PENDING.mkdir(parents=True, exist_ok=True)
        tmp.write_text(data, encoding="utf-8")
        n = ingest_file(tmp, sync=sync, export=export)
        print(f"Ingested {n} record(s) from stdin")
        return 0

    if args.file:
        n = ingest_file(args.file, sync=sync, export=export)
        print(f"Ingested {n} record(s) from {args.file}")
        return 0

    n = ingest_pending(sync=sync, export=export)
    print(f"Ingested {n} record(s) from pending/external queues")
    return 0


if __name__ == "__main__":
    sys.exit(main())
