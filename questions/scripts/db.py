"""SQLite connection, registry validation, question CRUD, audit log."""

from __future__ import annotations

import json
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from paths import (
    DB_PATH,
    FORBIDDEN_INGEST_ROOTS,
    GENERATED_DIR,
    REGISTRIES_DIR,
    SCHEMA_PATH,
    ALLOWED_INGEST_ROOTS,
    IGNORE_EXTENSIONS,
)

VALID_TYPES = {"open", "single", "multi", "scale", "sort", "fill", "agreement"}
OPTION_TYPES_REQUIRING_OPTIONS = {"agreement", "single", "multi"}
VALID_INTERACTIONS = {
    "story", "self_report", "scenario", "comparison", "rating", "reflection", "future",
}
VALID_STATUS = {"active", "candidate", "deprecated"}
VALID_DEPTH = {"shallow", "medium", "deep"}
RELATION_TYPES = {"duplicate", "variant", "followup", "similar"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_connection(*, readonly: bool = False) -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}. Run: python questions/scripts/init_db.py",
        )
    uri = f"file:{DB_PATH.as_posix()}?mode=ro" if readonly else None
    conn = sqlite3.connect(DB_PATH if not readonly else uri, uri=readonly)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_database(*, force: bool = False) -> Path:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists() and not force:
        return DB_PATH
    if force and DB_PATH.exists():
        DB_PATH.unlink()
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(schema)
        conn.commit()
    finally:
        conn.close()
    return DB_PATH


def set_meta(key: str, value: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO db_meta (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )
        conn.commit()
    finally:
        conn.close()


def get_meta(key: str) -> str | None:
    conn = get_connection(readonly=True)
    try:
        row = conn.execute("SELECT value FROM db_meta WHERE key=?", (key,)).fetchone()
        return row["value"] if row else None
    finally:
        conn.close()


def load_registry(name: str) -> dict[str, Any]:
    path = REGISTRIES_DIR / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Registry not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: registry root must be a mapping")
    entries = data.get("entries") or []
    ids: set[str] = set()
    aliases: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        entry_id = entry.get("id")
        if not entry_id:
            continue
        alias_of = entry.get("alias_of")
        if alias_of:
            aliases[str(entry_id)] = str(alias_of)
            ids.add(str(entry_id))
        else:
            ids.add(str(entry_id))
    return {
        "version": data.get("version"),
        "ids": ids,
        "aliases": aliases,
        "raw": data,
    }


def load_registries() -> dict[str, Any]:
    prereq = load_registry("prerequisites")
    tags = load_registry("tags")
    return {
        "prerequisites": prereq,
        "tags": tags,
        "valid_prerequisite_ids": prereq["ids"] | set(prereq["aliases"].values()),
        "valid_tag_ids": tags["ids"],
    }


def validate_question_refs(
    tags: list[str] | None,
    prerequisites: list[str] | None,
    registries: dict[str, Any] | None = None,
) -> list[str]:
    registries = registries or load_registries()
    errors: list[str] = []
    for t in tags or []:
        if t not in registries["valid_tag_ids"]:
            errors.append(f"unknown tag '{t}'")
    for p in prerequisites or []:
        if p not in registries["valid_prerequisite_ids"]:
            errors.append(f"unknown prerequisite '{p}'")
    return errors


def validate_options(options: Any, qtype: str) -> list[str]:
    """Validate options shape for ingest/sync. See 整理规范-v1.0.md §jsonl 字段契约."""
    errors: list[str] = []
    if options is None:
        if qtype in OPTION_TYPES_REQUIRING_OPTIONS:
            errors.append(
                f"type '{qtype}' requires options as [{{\"key\":\"…\",\"text\":\"…\"}},…]",
            )
        return errors
    if not isinstance(options, list):
        errors.append("options must be an array")
        return errors
    for i, opt in enumerate(options):
        if isinstance(opt, str):
            errors.append(
                f"options[{i}] is a string; use {{\"key\":\"1\",\"text\":\"…\"}} objects "
                "(see questions/整理规范-v1.0.md §jsonl 字段契约)",
            )
            continue
        if not isinstance(opt, dict):
            errors.append(f"options[{i}] must be an object with key and text")
            continue
        if not str(opt.get("key", "")).strip() or not str(opt.get("text", "")).strip():
            errors.append(f"options[{i}] missing required key or text")
    return errors


def validate_ingest_path(path: Path) -> None:
    resolved = path.resolve()
    for forbidden in FORBIDDEN_INGEST_ROOTS:
        if forbidden.exists():
            try:
                resolved.relative_to(forbidden.resolve())
                raise ValueError(f"ingest forbidden path under {forbidden}: {path}")
            except ValueError as e:
                if "forbidden" in str(e):
                    raise
    allowed = False
    for root in ALLOWED_INGEST_ROOTS:
        if root.exists():
            try:
                resolved.relative_to(root.resolve())
                allowed = True
                break
            except ValueError:
                continue
    if not allowed:
        raise ValueError(
            f"ingest path not under allowed roots {ALLOWED_INGEST_ROOTS}: {path}",
        )
    if path.suffix.lower() in IGNORE_EXTENSIONS:
        raise ValueError(f"ingest forbidden extension: {path.suffix}")


def row_to_dict(row: sqlite3.Row, conn: sqlite3.Connection) -> dict[str, Any]:
    d = dict(row)
    uid = d["uid"]
    tags = [r[0] for r in conn.execute(
        "SELECT tag FROM question_tags WHERE question_uid=? ORDER BY tag", (uid,),
    ).fetchall()]
    prereqs = [r[0] for r in conn.execute(
        "SELECT prerequisite_id FROM question_prerequisites WHERE question_uid=? ORDER BY prerequisite_id",
        (uid,),
    ).fetchall()]
    related_rows = conn.execute(
        """SELECT q.id, r.relation_type FROM question_relations r
           JOIN questions q ON q.uid = r.target_uid
           WHERE r.source_uid=?""",
        (uid,),
    ).fetchall()
    related = [r[0] for r in related_rows] if related_rows else None
    options = json.loads(d["options_json"]) if d.get("options_json") else None
    slug = d["category"]
    from paths import FILE_TO_CATEGORY
    label = next((lbl for _, (s, lbl) in FILE_TO_CATEGORY.items() if s == slug), slug)
    source_file = next((fn for fn, (s, _) in FILE_TO_CATEGORY.items() if s == slug), "")
    return {
        "uid": uid,
        "id": d["id"],
        "text": d["question"],
        "question": d["question"],
        "category": d["category"],
        "category_label": label,
        "subcategory": d["subcategory"],
        "type": d["type"],
        "interaction": d["interaction"],
        "source": d["source"],
        "status": d["status"],
        "depth": d["depth"],
        "validation": bool(d["validation"]),
        "order": d["order_num"],
        "order_num": d["order_num"],
        "deprecated_reason": d["deprecated_reason"],
        "superseded_by": d["superseded_by"],
        "notes": d["notes"],
        "tags": tags or None,
        "prerequisites": prereqs or None,
        "related": related,
        "options": options,
        "scale": d["scale_note"],
        "scale_note": d["scale_note"],
        "source_file": source_file,
        "created_at": d["created_at"],
        "updated_at": d["updated_at"],
    }


def fetch_question_by_id(conn: sqlite3.Connection, qid: str) -> dict[str, Any] | None:
    row = conn.execute("SELECT * FROM questions WHERE id=?", (qid,)).fetchone()
    if not row:
        row = conn.execute("SELECT * FROM questions WHERE uid=?", (qid,)).fetchone()
    return row_to_dict(row, conn) if row else None


def fetch_all_questions(
    conn: sqlite3.Connection | None = None,
    *,
    status_filter: set[str] | None = None,
) -> list[dict[str, Any]]:
    own = conn is None
    conn = conn or get_connection(readonly=True)
    try:
        sql = "SELECT * FROM questions"
        params: list[Any] = []
        if status_filter:
            placeholders = ",".join("?" * len(status_filter))
            sql += f" WHERE status IN ({placeholders})"
            params.extend(sorted(status_filter))
        sql += " ORDER BY id"
        rows = conn.execute(sql, params).fetchall()
        return [row_to_dict(r, conn) for r in rows]
    finally:
        if own:
            conn.close()


def _next_id_for_category(conn: sqlite3.Connection, category: str) -> str:
    from paths import FILE_TO_CATEGORY
    prefix_map = {
        "real": "REAL", "emo": "EMO", "dec": "DEC", "sta": "STA",
        "self": "SELF", "val": "VAL", "oth": "OTH",
    }
    prefix = prefix_map.get(category, "OTH")
    rows = conn.execute(
        "SELECT id FROM questions WHERE id LIKE ?",
        (f"Q-{prefix}-%",),
    ).fetchall()
    max_num = 0
    for r in rows:
        parts = r[0].split("-")
        if len(parts) == 3 and parts[2].isdigit():
            max_num = max(max_num, int(parts[2]))
    return f"Q-{prefix}-{max_num + 1:03d}"


def new_uid(conn: sqlite3.Connection) -> str:
    while True:
        uid = secrets.token_hex(4)
        if not conn.execute("SELECT 1 FROM questions WHERE uid=?", (uid,)).fetchone():
            return uid


def insert_question_record(
    conn: sqlite3.Connection,
    data: dict[str, Any],
    *,
    registries: dict[str, Any] | None = None,
) -> str:
    registries = registries or load_registries()
    tags = data.get("tags")
    prereqs = data.get("prerequisites")
    errs = validate_question_refs(tags, prereqs, registries)
    if errs:
        raise ValueError("; ".join(errs))

    now = utc_now()
    uid = data.get("uid") or new_uid(conn)
    qid = data.get("id")
    if not qid:
        qid = _next_id_for_category(conn, data["category"])

    qtype = data.get("type", "open")
    if qtype not in VALID_TYPES:
        raise ValueError(f"invalid type '{qtype}'")
    status = data.get("status", "active")
    if status not in VALID_STATUS:
        raise ValueError(f"invalid status '{status}'")
    interaction = data.get("interaction")
    if interaction is not None and interaction not in VALID_INTERACTIONS:
        raise ValueError(f"invalid interaction '{interaction}'")
    depth = data.get("depth")
    if depth is not None and depth not in VALID_DEPTH:
        raise ValueError(f"invalid depth '{depth}'")

    text = data.get("question") or data.get("text")
    if not text or not str(text).strip():
        raise ValueError("empty question text")

    for field in ("category", "subcategory"):
        if not data.get(field) or not str(data[field]).strip():
            raise ValueError(f"missing required field '{field}'")

    options = data.get("options")
    opt_errs = validate_options(options, qtype)
    if opt_errs:
        raise ValueError("; ".join(opt_errs))

    options_json = json.dumps(options, ensure_ascii=False) if options else None

    conn.execute(
        """INSERT INTO questions (
            uid, id, question, category, subcategory, type, interaction, source,
            status, depth, validation, order_num, deprecated_reason, superseded_by,
            notes, options_json, scale_note, created_at, updated_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            uid, qid, str(text).strip(), data["category"], data["subcategory"],
            qtype, interaction, data.get("source"), status, depth,
            1 if data.get("validation") else 0,
            data.get("order") or data.get("order_num"),
            data.get("deprecated_reason"), data.get("superseded_by"),
            data.get("notes"), options_json,
            data.get("scale") or data.get("scale_note"),
            data.get("created_at") or now, data.get("updated_at") or now,
        ),
    )
    for tag in tags or []:
        conn.execute(
            "INSERT OR IGNORE INTO question_tags (question_uid, tag) VALUES (?,?)",
            (uid, tag),
        )
    for p in prereqs or []:
        conn.execute(
            "INSERT OR IGNORE INTO question_prerequisites (question_uid, prerequisite_id) VALUES (?,?)",
            (uid, p),
        )
    return uid


def update_question_record(
    conn: sqlite3.Connection,
    qid: str,
    changes: dict[str, Any],
    *,
    registries: dict[str, Any] | None = None,
) -> dict[str, Any]:
    before = fetch_question_by_id(conn, qid)
    if not before:
        raise ValueError(f"question not found: {qid}")

    registries = registries or load_registries()
    merged = {**before, **changes}
    errs = validate_question_refs(merged.get("tags"), merged.get("prerequisites"), registries)
    if errs:
        raise ValueError("; ".join(errs))

    qtype = merged.get("type", "open")
    opt_errs = validate_options(merged.get("options"), qtype)
    if opt_errs:
        raise ValueError("; ".join(opt_errs))

    now = utc_now()
    uid = before["uid"]
    text = merged.get("question") or merged.get("text")
    options = merged.get("options")
    options_json = json.dumps(options, ensure_ascii=False) if options else None

    conn.execute(
        """UPDATE questions SET
            question=?, category=?, subcategory=?, type=?, interaction=?, source=?,
            status=?, depth=?, validation=?, order_num=?, deprecated_reason=?,
            superseded_by=?, notes=?, options_json=?, scale_note=?, updated_at=?
        WHERE uid=?""",
        (
            str(text).strip(), merged["category"], merged["subcategory"],
            merged["type"], merged.get("interaction"), merged.get("source"),
            merged["status"], merged.get("depth"),
            1 if merged.get("validation") else 0,
            merged.get("order") or merged.get("order_num"),
            merged.get("deprecated_reason"), merged.get("superseded_by"),
            merged.get("notes"), options_json,
            merged.get("scale") or merged.get("scale_note"),
            now, uid,
        ),
    )
    conn.execute("DELETE FROM question_tags WHERE question_uid=?", (uid,))
    for tag in merged.get("tags") or []:
        conn.execute(
            "INSERT INTO question_tags (question_uid, tag) VALUES (?,?)", (uid, tag),
        )
    conn.execute("DELETE FROM question_prerequisites WHERE question_uid=?", (uid,))
    for p in merged.get("prerequisites") or []:
        conn.execute(
            "INSERT INTO question_prerequisites (question_uid, prerequisite_id) VALUES (?,?)",
            (uid, p),
        )
    after = fetch_question_by_id(conn, uid)
    assert after
    return {"before": before, "after": after}


def add_relation(
    conn: sqlite3.Connection,
    source_id: str,
    target_id: str,
    relation_type: str,
) -> None:
    if relation_type not in RELATION_TYPES:
        raise ValueError(f"invalid relation_type '{relation_type}'")
    src = fetch_question_by_id(conn, source_id)
    tgt = fetch_question_by_id(conn, target_id)
    if not src or not tgt:
        raise ValueError("source or target question not found")
    conn.execute(
        """INSERT OR IGNORE INTO question_relations
           (source_uid, target_uid, relation_type) VALUES (?,?,?)""",
        (src["uid"], tgt["uid"], relation_type),
    )
    if relation_type == "duplicate":
        conn.execute(
            """INSERT OR IGNORE INTO question_relations
               (source_uid, target_uid, relation_type) VALUES (?,?,?)""",
            (tgt["uid"], src["uid"], relation_type),
        )


def append_audit(
    tool: str,
    cmd: str,
    before_state: dict[str, Any] | None,
    after_state: dict[str, Any] | None,
    changes: dict[str, Any] | None = None,
) -> int:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    log_path = GENERATED_DIR / "audit.log"
    audit_id = 1
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    audit_id = max(audit_id, json.loads(line).get("audit_id", 0) + 1)
                except json.JSONDecodeError:
                    pass
    entry = {
        "audit_id": audit_id,
        "ts": utc_now(),
        "tool": tool,
        "cmd": cmd,
        "uid": (after_state or before_state or {}).get("uid"),
        "id": (after_state or before_state or {}).get("id"),
        "before_state": before_state,
        "after_state": after_state,
        "changes": changes,
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return audit_id


def post_write_hooks(*, sync: bool = True, export: bool = True) -> None:
    if sync:
        from sync_categories import sync_categories
        sync_categories()
    if export:
        from export_json import export_json
        export_json()
