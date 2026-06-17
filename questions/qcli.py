#!/usr/bin/env python3
"""Question CLI — daily CRUD, review loop, registry browse."""

from __future__ import annotations

import json
import sys
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # pyright: ignore[reportAttributeAccessIssue]
    sys.stderr.reconfigure(encoding="utf-8")  # pyright: ignore[reportAttributeAccessIssue]

SCRIPTS = Path(__file__).resolve().parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import click  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402

from db import (  # noqa: E402
    RELATION_TYPES,
    add_relation,
    append_audit,
    fetch_all_questions,
    fetch_question_by_id,
    get_connection,
    get_meta,
    load_registries,
    post_write_hooks,
    update_question_record,
    utc_now,
    validate_ingest_path,
)
from paths import DB_PATH, GENERATED_DIR, REGISTRIES_DIR  # noqa: E402

console = Console()


def _json_out(data: dict, json_output: bool) -> None:
    if json_output:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))


def _resolve_q(conn, ref: str):
    q = fetch_question_by_id(conn, ref)
    if not q:
        raise click.ClickException(f"question not found: {ref}")
    return q


@click.group()
def cli():
    """Questions subsystem cockpit (qcli)."""


@cli.command("list")
@click.option("--category", "-c", help="Category slug e.g. real")
@click.option("--tag", "-t", help="Filter by tag")
@click.option("--status", default="active", help="Status filter (active|candidate|deprecated|all)")
@click.option("--limit", default=20, type=int)
@click.option("--format", "fmt", type=click.Choice(["table", "json"]), default="table")
def list_cmd(category, tag, status, limit, fmt):
    """List questions (read-only)."""
    conn = get_connection(readonly=True)
    try:
        sf = None if status == "all" else {status} if status != "active" else {"active", "candidate"}
        qs = fetch_all_questions(conn, status_filter=sf)
        if category:
            qs = [q for q in qs if q["category"] == category]
        if tag:
            qs = [q for q in qs if tag in (q.get("tags") or [])]
        qs = qs[:limit]
        if fmt == "json":
            click.echo(json.dumps(qs, ensure_ascii=False, indent=2))
            return
        table = Table(title=f"Questions (showing {len(qs)})")
        table.add_column("ID")
        table.add_column("Subcategory")
        table.add_column("Question", max_width=60)
        table.add_column("Tags")
        for q in qs:
            text = q["text"].replace("\n", " ")[:60]
            tags = ",".join(q.get("tags") or [])[:20]
            table.add_row(q["id"], q["subcategory"], text, tags)
        console.print(table)
    finally:
        conn.close()


@cli.command("show")
@click.argument("ref")
@click.option("--json-output", is_flag=True)
def show_cmd(ref, json_output):
    """Show one question."""
    conn = get_connection(readonly=True)
    try:
        q = _resolve_q(conn, ref)
        if json_output:
            _json_out({"ok": True, "question": q}, True)
        else:
            console.print(f"[bold]{q['id']}[/bold] uid={q['uid']}")
            console.print(f"category={q['category']} · {q['subcategory']} · status={q['status']}")
            if q.get("tags"):
                console.print(f"tags: {', '.join(q['tags'])}")
            if q.get("prerequisites"):
                console.print(f"prerequisites: {', '.join(q['prerequisites'])}")
            console.print(q["text"])
    finally:
        conn.close()


@cli.command("search")
@click.argument("query")
@click.option("--limit", default=10, type=int)
def search_cmd(query, limit):
    """FTS search on question text."""
    conn = get_connection(readonly=True)
    try:
        rows = conn.execute(
            """SELECT q.id, q.question FROM questions_fts f
               JOIN questions q ON q.rowid = f.rowid
               WHERE questions_fts MATCH ?
               LIMIT ?""",
            (query, limit),
        ).fetchall()
        for r in rows:
            text = r[1].replace("\n", " ")[:80]
            console.print(f"{r[0]}: {text}")
        if not rows:
            console.print("[dim]No matches[/dim]")
    finally:
        conn.close()


@cli.group("registry")
def registry_group():
    """Browse registries (YAML is source of truth)."""


@registry_group.command("list")
@click.argument("kind", type=click.Choice(["tags", "prerequisites"]))
def registry_list(kind):
    data = load_registries()[kind]["raw"]
    table = Table(title=kind)
    table.add_column("id")
    table.add_column("label")
    for entry in data.get("entries") or []:
        if isinstance(entry, dict) and entry.get("id"):
            table.add_row(str(entry["id"]), str(entry.get("label") or entry.get("name") or ""))
    console.print(table)


@registry_group.command("show")
@click.argument("kind", type=click.Choice(["tag", "prerequisite"]))
@click.argument("entry_id")
def registry_show(kind, entry_id):
    key = "tags" if kind == "tag" else "prerequisites"
    data = load_registries()[key]["raw"]
    for entry in data.get("entries") or []:
        if isinstance(entry, dict) and entry.get("id") == entry_id:
            click.echo(json.dumps(entry, ensure_ascii=False, indent=2))
            return
    raise click.ClickException(f"{kind} not found: {entry_id}")


@cli.command("edit")
@click.argument("ref")
@click.option("--set", "sets", multiple=True, help="key=value")
@click.option("--add-tag", multiple=True)
@click.option("--remove-tag", multiple=True)
@click.option("--json-output", is_flag=True)
@click.option("--no-sync", is_flag=True)
@click.option("--no-export", is_flag=True)
def edit_cmd(ref, sets, add_tag, remove_tag, json_output, no_sync, no_export):
    """Edit one question."""
    conn = get_connection()
    try:
        q = _resolve_q(conn, ref)
        changes: dict = {}
        for s in sets:
            if "=" not in s:
                raise click.ClickException(f"invalid --set: {s}")
            k, v = s.split("=", 1)
            if k in ("validation",):
                changes[k] = v.lower() in ("true", "1", "yes")
            elif k == "order":
                changes["order"] = int(v)
            else:
                changes[k] = v
        tags = list(q.get("tags") or [])
        for t in add_tag:
            if t not in tags:
                tags.append(t)
        for t in remove_tag:
            if t in tags:
                tags.remove(t)
        if add_tag or remove_tag:
            changes["tags"] = tags or None
        result = update_question_record(conn, ref, changes)
        conn.commit()
        audit_id = append_audit("qcli", "edit", result["before"], result["after"], changes)
        if not no_sync or not no_export:
            post_write_hooks(sync=not no_sync, export=not no_export)
        out = {
            "ok": True,
            "action": "edit",
            "id": result["after"]["id"],
            "uid": result["after"]["uid"],
            "changes": changes,
            "synced_categories": not no_sync,
            "audit_id": audit_id,
        }
        if json_output:
            _json_out(out, True)
        else:
            console.print(f"Updated {result['after']['id']} (audit #{audit_id})")
    finally:
        conn.close()


@cli.command("relate")
@click.argument("ref")
@click.option("--duplicate-of")
@click.option("--followup-to")
@click.option("--similar-to")
@click.option("--json-output", is_flag=True)
@click.option("--no-sync", is_flag=True)
def relate_cmd(ref, duplicate_of, followup_to, similar_to, json_output, no_sync):
    conn = get_connection()
    try:
        before = _resolve_q(conn, ref)
        target = duplicate_of or followup_to or similar_to
        if not target:
            raise click.ClickException("specify --duplicate-of, --followup-to, or --similar-to")
        rtype = "duplicate" if duplicate_of else ("followup" if followup_to else "similar")
        add_relation(conn, ref, target, rtype)
        conn.commit()
        after = _resolve_q(conn, ref)
        audit_id = append_audit("qcli", "relate", before, after, {"target": target, "type": rtype})
        if not no_sync:
            post_write_hooks(sync=True, export=True)
        out = {"ok": True, "id": before["id"], "relation": rtype, "target": target, "audit_id": audit_id}
        if json_output:
            _json_out(out, True)
        else:
            console.print(f"Relation {rtype} → {target} (audit #{audit_id})")
    finally:
        conn.close()


def _session_path(name: str) -> Path:
    d = GENERATED_DIR / "review_sessions"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{name}.json"


def _load_session(name: str) -> dict:
    p = _session_path(name)
    if not p.exists():
        raise click.ClickException(f"session not found: {name}")
    return json.loads(p.read_text(encoding="utf-8"))


def _save_session(doc: dict) -> None:
    doc["updated_at"] = utc_now()
    _session_path(doc["session"]).write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )


@cli.command("review")
@click.option("--batch", default=10, type=int)
@click.option("--category", "-c")
@click.option("--status", default="active")
@click.option("--session", "session_name", help="Session name for resume")
@click.option("--resume", help="Resume existing session")
@click.option("--dry-run", is_flag=True)
@click.option("--json-output", is_flag=True)
@click.option("--ci", is_flag=True)
def review_cmd(batch, category, status, session_name, resume, dry_run, json_output, ci):
    """Interactive batch review loop."""
    if resume:
        doc = _load_session(resume)
        batch = doc.get("batch_size", batch)
        category = doc.get("filter", {}).get("category", category)
        status = doc.get("filter", {}).get("status", status)
        session_name = resume
        start_idx = doc.get("cursor_index", 0)
        processed = set(doc.get("processed") or [])
        skipped = set(doc.get("skipped") or [])
    else:
        session_name = session_name or f"review_{utc_now()[:10].replace('-', '')}"
        start_idx = 0
        processed = set()
        skipped = set()
        doc = {
            "session": session_name,
            "filter": {"category": category, "status": status},
            "batch_size": batch,
            "cursor_index": 0,
            "processed": [],
            "skipped": [],
            "defer_sync": True,
        }

    conn = get_connection(readonly=True)
    try:
        sf = {"active", "candidate"} if status == "active" else {status}
        qs = fetch_all_questions(conn, status_filter=sf)
        if category:
            qs = [q for q in qs if q["category"] == category]
        qs = [q for q in qs if q["id"] not in processed and q["id"] not in skipped]
    finally:
        conn.close()

    if ci or json_output:
        chunk = qs[start_idx : start_idx + batch]
        _json_out({"ok": True, "session": session_name, "questions": chunk}, True)
        return

    idx = start_idx
    changed = False
    while idx < len(qs) and idx < start_idx + batch:
        q = qs[idx]
        console.print(f"\n[{idx + 1}/{min(len(qs), start_idx + batch)}] [bold]{q['id']}[/bold]")
        console.print(q["text"][:200].replace("\n", " "))
        console.print(
            f"cat:{q['category']} · {q['subcategory']} · tags:{','.join(q.get('tags') or [])}",
        )
        if dry_run:
            action = click.prompt(
                "(e)编辑 (s)跳过 (q)退出", default="s", show_default=True,
            )
        else:
            action = click.prompt(
                "(e)编辑题干 (d)废弃 (s)跳过 (q)退出", default="s", show_default=True,
            )
        action = action.strip().lower()
        if action == "q":
            doc["cursor_index"] = idx
            doc["processed"] = list(processed)
            doc["skipped"] = list(skipped)
            _save_session(doc)
            console.print(f"Session saved: {session_name} (--resume {session_name})")
            break
        if action == "s":
            skipped.add(q["id"])
            idx += 1
            continue
        if action == "e" and not dry_run:
            new_text = click.prompt("新题干", default=q["text"])
            if click.confirm("确认更新?", default=True):
                conn = get_connection()
                try:
                    result = update_question_record(conn, q["id"], {"question": new_text, "text": new_text})
                    conn.commit()
                    append_audit("qcli", "review-edit", result["before"], result["after"], {"question": new_text})
                    changed = True
                    processed.add(q["id"])
                finally:
                    conn.close()
            idx += 1
            continue
        if action == "d" and not dry_run:
            conn = get_connection()
            try:
                result = update_question_record(conn, q["id"], {"status": "deprecated"})
                conn.commit()
                append_audit("qcli", "review-deprecate", result["before"], result["after"], {})
                changed = True
                processed.add(q["id"])
            finally:
                conn.close()
            idx += 1
            continue
        idx += 1

    doc["cursor_index"] = idx
    doc["processed"] = list(processed)
    doc["skipped"] = list(skipped)
    _save_session(doc)

    if changed and not dry_run:
        post_write_hooks(sync=True, export=True)
        console.print("Synced categories + exported json")


@cli.command("ingest")
@click.option("--file", type=click.Path(exists=True, path_type=Path))
@click.option("--stdin", is_flag=True)
@click.option("--no-sync", is_flag=True)
def ingest_cmd(file, stdin, no_sync):
    """Ingest jsonl (delegates to ingest.py)."""
    from ingest import ingest_file, ingest_pending
    sync = not no_sync
    if stdin:
        data = sys.stdin.read()
        from paths import IMPORTS_PENDING
        from datetime import datetime, timezone
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        tmp = IMPORTS_PENDING / f"_qcli_stdin_{ts}.jsonl"
        IMPORTS_PENDING.mkdir(parents=True, exist_ok=True)
        tmp.write_text(data, encoding="utf-8")
        n = ingest_file(tmp, sync=sync, export=sync)
    elif file:
        n = ingest_file(file, sync=sync, export=sync)
    else:
        n = ingest_pending(sync=sync, export=sync)
    console.print(f"Ingested {n} record(s)")


@cli.command("doctor")
def doctor_cmd():
    """Health check."""
    from manage import cmd_check
    import argparse
    sys.exit(cmd_check(argparse.Namespace()))


if __name__ == "__main__":
    cli()
