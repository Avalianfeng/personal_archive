#!/usr/bin/env python3
"""Question CLI — Agent-first CRUD and queries."""

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
    add_relation,
    append_audit,
    fetch_all_questions,
    fetch_question_by_id,
    get_connection,
    load_registries,
    post_write_hooks,
    update_question_record,
    validate_ingest_path,
)
from paths import AGENT_VIEWS_DIR, GENERATED_DIR  # noqa: E402

console = Console()
AGENT_DIR = AGENT_VIEWS_DIR


def _want_json(ctx: click.Context) -> bool:
    return bool(ctx.obj.get("json_output")) if ctx.obj else False


def _emit(data: dict | list, ctx: click.Context) -> None:
    click.echo(json.dumps(data, ensure_ascii=False, indent=2))


def _resolve_q(conn, ref: str):
    q = fetch_question_by_id(conn, ref)
    if not q:
        raise click.ClickException(f"question not found: {ref}")
    return q


def _pick_fields(q: dict, fields: str | None) -> dict:
    if not fields:
        return q
    keys = [k.strip() for k in fields.split(",") if k.strip()]
    return {k: q.get(k) for k in keys}


@click.group()
@click.option(
    "--json-output",
    is_flag=True,
    envvar="QCLI_JSON",
    help="JSON output (default for Agent; set QCLI_JSON=1)",
)
@click.option("--human", is_flag=True, help="Human-readable Rich/text output")
@click.pass_context
def cli(ctx, json_output, human):
    """Questions subsystem — Agent-first CLI."""
    ctx.ensure_object(dict)
    ctx.obj["json_output"] = False if human else True
    if json_output:
        ctx.obj["json_output"] = True


@cli.command("list")
@click.option("--category", "-c", help="Category slug e.g. real")
@click.option("--tag", "-t", help="Filter by tag")
@click.option("--status", default="active", help="Status filter (active|candidate|deprecated|all)")
@click.option("--limit", default=20, type=int)
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["compact", "json", "table"]),
    default=None,
    help="Output format (default: compact if --json-output else table)",
)
@click.pass_context
def list_cmd(ctx, category, tag, status, limit, fmt):
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

        use_json = _want_json(ctx)
        fmt = fmt or ("compact" if use_json else "table")

        if fmt == "json":
            _emit(qs, ctx)
            return
        if fmt == "compact":
            lines = [
                {"id": q["id"], "text": (q.get("text") or "").replace("\n", " ").strip()}
                for q in qs
            ]
            if use_json:
                _emit({"ok": True, "count": len(lines), "questions": lines}, ctx)
            else:
                for row in lines:
                    click.echo(f"{row['id']}\t{row['text']}")
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
@click.argument("ref", required=False)
@click.option("--ids", help="Comma-separated question ids")
@click.option("--fields", help="Comma-separated fields to include")
@click.pass_context
def show_cmd(ctx, ref, ids, fields):
    """Show one or more questions."""
    id_list: list[str] = []
    if ids:
        id_list = [x.strip() for x in ids.split(",") if x.strip()]
    elif ref:
        id_list = [ref]
    else:
        raise click.ClickException("provide ref argument or --ids")

    conn = get_connection(readonly=True)
    try:
        items = []
        for qid in id_list:
            q = _pick_fields(_resolve_q(conn, qid), fields)
            items.append(q)
        if _want_json(ctx):
            if len(items) == 1:
                _emit({"ok": True, "question": items[0]}, ctx)
            else:
                _emit({"ok": True, "questions": items}, ctx)
        else:
            for q in items:
                console.print(f"[bold]{q['id']}[/bold] uid={q.get('uid', '')}")
                console.print(
                    f"category={q.get('category')} · {q.get('subcategory')} · status={q.get('status')}",
                )
                if q.get("tags"):
                    console.print(f"tags: {', '.join(q['tags'])}")
                console.print(q.get("text") or q.get("question") or "")
    finally:
        conn.close()


@cli.command("search")
@click.argument("query")
@click.option("--limit", default=10, type=int)
@click.pass_context
def search_cmd(ctx, query, limit):
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
        results = [
            {"id": r[0], "text": r[1].replace("\n", " ").strip()}
            for r in rows
        ]
        if _want_json(ctx):
            _emit({"ok": True, "query": query, "results": results}, ctx)
            return
        for row in results:
            click.echo(f"{row['id']}: {row['text'][:80]}")
        if not results:
            console.print("[dim]No matches[/dim]")
    finally:
        conn.close()


@cli.command("dump")
@click.option("--category", "-c", help="Category slug; omit for full bank_compact.md")
@click.option("--batch", is_flag=True, help="Read batch_delta_compact.md (latest accept batch)")
@click.pass_context
def dump_cmd(ctx, category, batch):
    """Print Agent compact view from 03-generated/01-agent-Agent视图/."""
    if batch:
        path = AGENT_DIR / "batch_delta_compact.md"
        if not path.exists():
            raise click.ClickException(
                "missing batch_delta_compact.md — run manage.py accept after ingesting a batch",
            )
    elif category:
        path = AGENT_DIR / "by_category" / f"{category}.md"
    else:
        path = AGENT_DIR / "bank_compact.md"
    if not path.exists():
        raise click.ClickException(
            f"missing {path.relative_to(GENERATED_DIR.parent)} — run manage.py sync first",
        )
    text = path.read_text(encoding="utf-8")
    if _want_json(ctx):
        _emit({"ok": True, "path": str(path.relative_to(GENERATED_DIR.parent)), "content": text}, ctx)
    else:
        click.echo(text, nl=False)


@cli.group("registry")
def registry_group():
    """Browse registries — prefer 03-generated-审计产物/registries.json for Agents."""


@registry_group.command("list")
@click.argument("kind", type=click.Choice(["tags", "prerequisites", "options_templates"]))
@click.pass_context
def registry_list(ctx, kind):
    data = load_registries()[kind]["raw"]
    entries = [
        {"id": e.get("id"), "label": e.get("label") or e.get("name") or ""}
        for e in (data.get("entries") or [])
        if isinstance(e, dict) and e.get("id")
    ]
    if _want_json(ctx):
        _emit({"ok": True, "kind": kind, "entries": entries}, ctx)
        return
    table = Table(title=kind)
    table.add_column("id")
    table.add_column("label")
    for entry in entries:
        table.add_row(str(entry["id"]), str(entry["label"]))
    console.print(table)


@registry_group.command("show")
@click.argument("kind", type=click.Choice(["tag", "prerequisite"]))
@click.argument("entry_id")
@click.pass_context
def registry_show(ctx, kind, entry_id):
    key = "tags" if kind == "tag" else "prerequisites"
    data = load_registries()[key]["raw"]
    for entry in data.get("entries") or []:
        if isinstance(entry, dict) and entry.get("id") == entry_id:
            if _want_json(ctx):
                _emit({"ok": True, "entry": entry}, ctx)
            else:
                click.echo(json.dumps(entry, ensure_ascii=False, indent=2))
            return
    raise click.ClickException(f"{kind} not found: {entry_id}")


def _apply_edit(ctx, ref, sets, add_tag, remove_tag, no_sync, no_export):
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
        if not (no_sync and no_export):
            post_write_hooks(sync=not no_sync, export=not no_export)
        return {
            "ok": True,
            "action": "edit",
            "id": result["after"]["id"],
            "uid": result["after"]["uid"],
            "changes": changes,
            "synced_categories": not no_sync,
            "audit_id": audit_id,
        }
    finally:
        conn.close()


@cli.command("edit")
@click.argument("ref")
@click.option("--set", "sets", multiple=True, help="key=value")
@click.option("--add-tag", multiple=True)
@click.option("--remove-tag", multiple=True)
@click.option("--no-sync", is_flag=True)
@click.option("--no-export", is_flag=True)
@click.pass_context
def edit_cmd(ctx, ref, sets, add_tag, remove_tag, no_sync, no_export):
    """Edit one question."""
    out = _apply_edit(ctx, ref, sets, add_tag, remove_tag, no_sync, no_export)
    if _want_json(ctx):
        _emit(out, ctx)
    else:
        console.print(f"Updated {out['id']} (audit #{out['audit_id']})")


@cli.command("relate")
@click.argument("ref")
@click.option("--duplicate-of")
@click.option("--followup-to")
@click.option("--similar-to")
@click.option("--no-sync", is_flag=True)
@click.pass_context
def relate_cmd(ctx, ref, duplicate_of, followup_to, similar_to, no_sync):
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
        if _want_json(ctx):
            _emit(out, ctx)
        else:
            console.print(f"Relation {rtype} → {target} (audit #{audit_id})")
    finally:
        conn.close()


@cli.command("review")
@click.option("--batch", default=10, type=int)
@click.option("--category", "-c")
@click.option("--status", default="active")
@click.option("--offset", default=0, type=int, help="Start index")
@click.pass_context
def review_cmd(ctx, batch, category, status, offset):
    """Deprecated: use `list --format compact` or `dump`. Returns JSON batch of questions."""
    conn = get_connection(readonly=True)
    try:
        sf = {"active", "candidate"} if status == "active" else {status}
        qs = fetch_all_questions(conn, status_filter=sf)
        if category:
            qs = [q for q in qs if q["category"] == category]
        chunk = qs[offset : offset + batch]
        out = {
            "ok": True,
            "deprecated_command": "use list --format compact or dump",
            "total": len(qs),
            "offset": offset,
            "batch": batch,
            "questions": chunk,
        }
        if _want_json(ctx):
            _emit(out, ctx)
        else:
            click.echo(json.dumps(out, ensure_ascii=False, indent=2))
    finally:
        conn.close()


@cli.command("ingest")
@click.option("--file", type=click.Path(exists=True, path_type=Path))
@click.option("--stdin", is_flag=True)
@click.option("--dry-run", is_flag=True, help="Validate jsonl only")
@click.option("--sync", is_flag=True, help="Sync categories + export after ingest")
@click.pass_context
def ingest_cmd(ctx, file, stdin, dry_run, sync):
    """Ingest jsonl — prefer manage accept for full batch."""
    from ingest import ingest_file, ingest_pending
    export = sync and not dry_run
    if stdin:
        data = sys.stdin.read()
        from paths import IMPORTS_PENDING
        from datetime import datetime, timezone
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        tmp = IMPORTS_PENDING / f"_qcli_stdin_{ts}.jsonl"
        IMPORTS_PENDING.mkdir(parents=True, exist_ok=True)
        tmp.write_text(data, encoding="utf-8")
        n = ingest_file(tmp, sync=sync, export=export, dry_run=dry_run)
    elif file:
        n = ingest_file(file, sync=sync, export=export, dry_run=dry_run)
    else:
        n = ingest_pending(sync=sync, export=export, dry_run=dry_run)
    label = "Validated" if dry_run else "Ingested"
    out = {"ok": True, "action": label.lower(), "count": n}
    if _want_json(ctx):
        _emit(out, ctx)
    else:
        console.print(f"{label} {n} record(s)")


@cli.command("doctor")
@click.pass_context
def doctor_cmd(ctx):
    """Health check — reads/writes 03-generated-审计产物/health.json."""
    from health_check import print_health_check, run_health_check

    health_path = GENERATED_DIR / "health.json"
    result = run_health_check()
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    from db import utc_now
    result["generated_at"] = utc_now()
    health_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if _want_json(ctx):
        _emit(result, ctx)
        sys.exit(0 if result.get("ok") else 1)
    sys.exit(print_health_check(result))


if __name__ == "__main__":
    cli()
