#!/usr/bin/env python3
"""Question Builder: compile categories/*.md → generated/*.json + stats + hints."""

from __future__ import annotations

import argparse
import json
import re
import secrets
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

QUESTIONS_DIR = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = QUESTIONS_DIR / "categories"
GENERATED_DIR = QUESTIONS_DIR / "generated"
REJECTED_DIR = QUESTIONS_DIR / "rejected"

FILE_TO_CATEGORY: dict[str, tuple[str, str]] = {
    "现实问题.md": ("real", "现实问题"),
    "情感问题.md": ("emo", "情感问题"),
    "决策问题.md": ("dec", "决策问题"),
    "状态问题.md": ("sta", "状态问题"),
    "自我认知.md": ("self", "自我认知"),
    "价值问题.md": ("val", "价值问题"),
    "其他.md": ("oth", "其他"),
}

PREFIX_TO_FILE = {
    "REAL": "现实问题.md",
    "EMO": "情感问题.md",
    "DEC": "决策问题.md",
    "STA": "状态问题.md",
    "SELF": "自我认知.md",
    "VAL": "价值问题.md",
    "OTH": "其他.md",
}

VALID_TYPES = {"open", "single", "multi", "scale", "sort", "fill", "agreement"}
VALID_INTERACTIONS = {
    "story", "self_report", "scenario", "comparison", "rating", "reflection", "future",
}
VALID_STATUS = {"active", "candidate", "deprecated"}
VALID_DEPTH = {"shallow", "medium", "deep"}
ID_PATTERN = re.compile(r"^Q-(REAL|EMO|DEC|STA|SELF|VAL|OTH)-(\d{3})$")
UID_PATTERN = re.compile(r"^[0-9a-f]{8}$")
OPTION_PATTERN = re.compile(r"^-\s*([A-Z])\.\s*(.+)$")
FM_BLOCK_PATTERN = re.compile(r"(?ms)^---\s*\n(.*?)\n---\s*\n")

DYADIC_PATTERNS = [
    re.compile(r"你最喜欢我的"),
    re.compile(r"你对我的"),
    re.compile(r"你对我的孩子们"),
    re.compile(r"你以我为荣"),
    re.compile(r"关于我，?你"),
    re.compile(r"关于我.*?从未问过"),
    re.compile(r"我们最后一次谈话"),
    re.compile(r"想对我说的"),
    re.compile(r"想告诉我|还没告诉我"),
    re.compile(r"给我或家里"),
    re.compile(r"你会如何形容我"),
    re.compile(r"你觉得我们有哪些相似"),
    re.compile(r"你觉得我们会失去联系"),
    re.compile(r"你对我的第一个记忆"),
    re.compile(r"你对我的第一印象"),
    re.compile(r"你不喜欢过我"),
    re.compile(r"如果一切可以重来，你会用不同的方式养育我"),
    re.compile(r"如果想给我或家里"),
    re.compile(r"对于多年以后聆听这段"),
    re.compile(r"如果.+今天在这里，你会问.+什么问题"),
]


def empty_to_none(value):
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


def new_uid(existing: set[str]) -> str:
    while True:
        uid = secrets.token_hex(4)
        if uid not in existing:
            return uid


def is_dyadic_candidate(text: str) -> bool:
    return any(p.search(text) for p in DYADIC_PATTERNS)


def normalize_text(text: str) -> str:
    t = re.sub(r"\s+", "", text.lower())
    t = re.sub(r"[？?！!。，,、；;：:\"\"''（）()\\[\\]/]", "", t)
    return t


def parse_options(body_lines: list[str]) -> tuple[str, list[dict[str, str]] | None, str | None]:
    text_lines: list[str] = []
    options: list[dict[str, str]] = []
    scale_note: str | None = None

    for line in body_lines:
        stripped = line.strip()
        if not stripped:
            if text_lines and not options:
                text_lines.append("")
            continue
        opt_match = OPTION_PATTERN.match(stripped)
        if opt_match:
            options.append({"key": opt_match.group(1), "text": opt_match.group(2).strip()})
            continue
        if stripped.startswith("（") and stripped.endswith("）") and not text_lines:
            scale_note = stripped
            continue
        text_lines.append(line.rstrip())

    text = "\n".join(text_lines).strip()
    if scale_note and text:
        text = f"{text}\n{scale_note}"
    elif scale_note and not text:
        text = scale_note

    return text, (options if options else None), scale_note


def normalize_frontmatter(meta: dict, file_slug: str, file_label: str, source_file: str) -> dict:
    errors: list[str] = []

    qid = meta.get("id")
    if not qid or not ID_PATTERN.match(str(qid)):
        errors.append(f"{source_file}: invalid or missing id")

    uid = empty_to_none(meta.get("uid"))
    if uid is not None and not UID_PATTERN.match(str(uid)):
        errors.append(f"{source_file} {qid}: invalid uid '{uid}'")

    category = meta.get("category")
    if category != file_slug:
        errors.append(f"{source_file} {qid}: category '{category}' != file slug '{file_slug}'")

    subcategory = meta.get("subcategory")
    if not subcategory or not str(subcategory).strip():
        errors.append(f"{source_file} {qid}: subcategory is required")

    qtype = meta.get("type")
    if qtype not in VALID_TYPES:
        errors.append(f"{source_file} {qid}: invalid type '{qtype}'")

    interaction = empty_to_none(meta.get("interaction"))
    if interaction is not None and interaction not in VALID_INTERACTIONS:
        errors.append(f"{source_file} {qid}: invalid interaction '{interaction}'")

    status = meta.get("status", "active")
    if status not in VALID_STATUS:
        errors.append(f"{source_file} {qid}: invalid status '{status}'")

    depth = empty_to_none(meta.get("depth"))
    if depth is not None and depth not in VALID_DEPTH:
        errors.append(f"{source_file} {qid}: invalid depth '{depth}'")

    order = meta.get("order")
    if order is not None and not isinstance(order, int):
        errors.append(f"{source_file} {qid}: order must be integer")

    tags = meta.get("tags")
    if tags is None:
        tags_out = None
    elif isinstance(tags, list):
        tags_out = [str(t) for t in tags if str(t).strip()]
    else:
        errors.append(f"{source_file} {qid}: tags must be a list")

    related = meta.get("related")
    if related is None:
        related_out = None
    elif isinstance(related, list):
        related_out = [str(r) for r in related if str(r).strip()]
    else:
        errors.append(f"{source_file} {qid}: related must be a list")

    validation = bool(meta.get("validation", False))

    if errors:
        raise ValueError("\n".join(errors))

    return {
        "uid": uid,
        "id": qid,
        "category": category,
        "category_label": file_label,
        "subcategory": str(subcategory).strip(),
        "type": qtype,
        "interaction": interaction,
        "source": empty_to_none(meta.get("source")),
        "tags": tags_out if tags is not None else None,
        "depth": depth,
        "validation": validation,
        "related": related_out,
        "status": status,
        "order": order,
        "superseded_by": empty_to_none(meta.get("superseded_by")),
        "deprecated_reason": empty_to_none(meta.get("deprecated_reason")),
        "source_file": source_file,
    }


def iter_blocks(path: Path):
    content = path.read_text(encoding="utf-8")
    for match in FM_BLOCK_PATTERN.finditer(content):
        meta = yaml.safe_load(match.group(1))
        if not isinstance(meta, dict) or "id" not in meta:
            continue
        body = content[match.end() :]
        next_fm = FM_BLOCK_PATTERN.search(body)
        body_text = body[: next_fm.start()] if next_fm else body
        body_lines: list[str] = []
        for line in body_text.splitlines():
            if line.startswith("## "):
                break
            body_lines.append(line)
        yield match, meta, body_lines, content


def parse_category_file(path: Path) -> list[dict]:
    if path.name not in FILE_TO_CATEGORY:
        return []

    slug, label = FILE_TO_CATEGORY[path.name]
    questions: list[dict] = []

    for _match, meta, body_lines, _content in iter_blocks(path):
        base = normalize_frontmatter(meta, slug, label, path.name)
        text, options, scale = parse_options(body_lines)
        if not text:
            raise ValueError(f"{path.name} {base['id']}: empty question text")
        base["text"] = text
        base["options"] = options
        base["scale"] = scale
        questions.append(base)

    return questions


def write_uids_to_files(dry_run: bool = False) -> int:
    existing_uids: set[str] = set()
    updated = 0

    for path in sorted(CATEGORIES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        content = path.read_text(encoding="utf-8")

        for match in FM_BLOCK_PATTERN.finditer(content):
            meta = yaml.safe_load(match.group(1))
            if isinstance(meta, dict) and empty_to_none(meta.get("uid")):
                existing_uids.add(str(meta["uid"]))

        new_content = content
        offset = 0
        file_changed = False

        for match in FM_BLOCK_PATTERN.finditer(content):
            meta = yaml.safe_load(match.group(1))
            if not isinstance(meta, dict) or "id" not in meta:
                continue
            if empty_to_none(meta.get("uid")):
                continue

            uid = new_uid(existing_uids)
            existing_uids.add(uid)
            fm_text = match.group(1)
            if fm_text.lstrip().startswith("uid:"):
                continue

            new_fm = f"uid: {uid}\n{fm_text}"
            start = match.start() + offset
            end = match.end() + offset
            replacement = f"---\n{new_fm}\n---\n"
            new_content = new_content[:start] + replacement + new_content[end:]
            offset += len(replacement) - (end - start)
            file_changed = True
            updated += 1

        if file_changed and not dry_run:
            path.write_text(new_content, encoding="utf-8")

    return updated


def compute_id_gaps(questions: list[dict]) -> dict[str, list[int]]:
    gaps: dict[str, list[int]] = {}
    by_prefix: dict[str, set[int]] = defaultdict(set)

    for q in questions:
        m = ID_PATTERN.match(q["id"])
        if m:
            by_prefix[m.group(1)].add(int(m.group(2)))

    for prefix, nums in sorted(by_prefix.items()):
        if not nums:
            continue
        missing = [n for n in range(1, max(nums) + 1) if n not in nums]
        if missing:
            gaps[prefix] = missing
    return gaps


def build_duplicate_hints(questions: list[dict]) -> dict:
    exact: dict[str, list[str]] = defaultdict(list)
    for q in questions:
        key = normalize_text(q["text"])
        exact[key].append(q["id"])

    exact_dups = [
        {"text_normalized": k, "ids": ids}
        for k, ids in exact.items()
        if len(ids) > 1
    ]

    return {
        "exact_text_duplicates": exact_dups,
        "count": len(exact_dups),
    }


def build_stats(questions: list[dict], include_deprecated: bool) -> dict:
    active = [q for q in questions if q["status"] in ("active", "candidate")]
    pool = questions if include_deprecated else active

    return {
        "total": len(pool),
        "total_including_deprecated": len(questions),
        "by_category": dict(Counter(q["category"] for q in pool)),
        "by_subcategory": dict(Counter(f"{q['category']}:{q['subcategory']}" for q in pool)),
        "by_source": dict(Counter(q["source"] or "(none)" for q in pool)),
        "by_status": dict(Counter(q["status"] for q in questions)),
        "by_type": dict(Counter(q["type"] for q in pool)),
        "missing_uid": [q["id"] for q in questions if not q.get("uid")],
        "id_gaps": compute_id_gaps(questions),
    }


def audit_dyadic(questions: list[dict]) -> list[dict]:
    hits = []
    for q in questions:
        if is_dyadic_candidate(q["text"]):
            hits.append({
                "id": q["id"],
                "uid": q.get("uid"),
                "source_file": q["source_file"],
                "text": q["text"],
                "reason": "intimate_dyadic",
            })
    return hits


def remove_questions_by_ids(ids: set[str]) -> list[dict]:
    removed: list[dict] = []

    for path in sorted(CATEGORIES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        content = path.read_text(encoding="utf-8")
        new_parts: list[str] = []
        last_end = 0

        for match, meta, body_lines, _full in iter_blocks(path):
            qid = meta.get("id")
            if qid in ids:
                slug, label = FILE_TO_CATEGORY[path.name]
                base = normalize_frontmatter(meta, slug, label, path.name)
                text, options, scale = parse_options(body_lines)
                base["text"] = text
                base["options"] = options
                base["scale"] = scale
                base["reject_reason"] = "intimate_dyadic"
                removed.append(base)
                new_parts.append(content[last_end : match.start()])
                last_end = match.end()
                body = content[match.end() :]
                next_fm = FM_BLOCK_PATTERN.search(body)
                last_end = match.end() + (next_fm.start() if next_fm else len(body))

        if removed and any(r["source_file"] == path.name and r["id"] in ids for r in removed):
            # rebuild file by filtering blocks
            blocks_to_keep: list[str] = []
            header_end = 0
            first_fm = FM_BLOCK_PATTERN.search(content)
            if first_fm:
                header_end = first_fm.start()
            header = content[:header_end]

            pos = header_end
            for match in FM_BLOCK_PATTERN.finditer(content):
                meta = yaml.safe_load(match.group(1))
                if isinstance(meta, dict) and meta.get("id") in ids:
                    continue
                blocks_to_keep.append(content[pos : match.end()] + _block_body(content, match))
                pos = match.end() + (FM_BLOCK_PATTERN.search(content[match.end() :]) or type("", (), {"start": lambda s: len(content[match.end():])})()).start() if False else 0

            # simpler: line-by-line rebuild
            out_chunks = [header.rstrip() + "\n\n" if header.strip() else ""]
            for match, meta, body_lines, _c in iter_blocks(path):
                if meta.get("id") in ids:
                    continue
                out_chunks.append(content[match.start() : match.end()])
                body = content[match.end() :]
                nxt = FM_BLOCK_PATTERN.search(body)
                body_text = body[: nxt.start()] if nxt else body
                out_chunks.append(body_text.rstrip() + "\n\n")

            path.write_text("".join(out_chunks).rstrip() + "\n", encoding="utf-8")

    return [r for r in removed if r["id"] in ids]


def _block_body(content: str, match: re.Match) -> str:
    body = content[match.end() :]
    nxt = FM_BLOCK_PATTERN.search(body)
    return body[: nxt.start()] if nxt else body


def append_to_system_unaskable(removed: list[dict]) -> None:
    path = REJECTED_DIR / "system_unaskable.md"
    if path.exists():
        existing = path.read_text(encoding="utf-8")
    else:
        existing = (
            "# 系统不可提问 · 淘汰题汇总\n\n"
            "> reason: `system_unaskable` · `intimate_dyadic`\n"
            "> 题干预设在场对话者（采访者↔被采访者），本系统无法复现。\n\n"
        )

    chunks = [existing.rstrip(), "\n"]
    for q in removed:
        uid_line = f"uid: {q['uid']}\n" if q.get("uid") else ""
        chunks.append(f"## {q['id']}\n\n---\n{uid_line}id: {q['id']}\n")
        chunks.append(f"category: {q['category']}\n")
        chunks.append(f"subcategory: {q['subcategory']}\n")
        chunks.append(f"source: {q.get('source') or 'StoryCorps'}\n")
        chunks.append("reject_reason: intimate_dyadic\nstatus: rejected\n---\n\n")
        chunks.append(q["text"] + "\n\n")

    path.write_text("".join(chunks), encoding="utf-8")


def load_all_questions() -> list[dict]:
    all_questions: list[dict] = []
    seen_ids: set[str] = set()
    seen_uids: set[str] = set()

    for path in sorted(CATEGORIES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        for q in parse_category_file(path):
            if q["id"] in seen_ids:
                raise ValueError(f"duplicate id {q['id']}")
            seen_ids.add(q["id"])
            if q.get("uid"):
                if q["uid"] in seen_uids:
                    raise ValueError(f"duplicate uid {q['uid']}")
                seen_uids.add(q["uid"])
            all_questions.append(q)

    all_questions.sort(key=lambda q: q["id"])
    return all_questions


def write_outputs(questions: list[dict], include_deprecated: bool) -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    export = questions if include_deprecated else [
        q for q in questions if q["status"] in ("active", "candidate")
    ]

    (GENERATED_DIR / "questions.json").write_text(
        json.dumps(export, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (GENERATED_DIR / "stats.json").write_text(
        json.dumps(build_stats(questions, include_deprecated), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (GENERATED_DIR / "duplicate_hints.json").write_text(
        json.dumps(build_duplicate_hints(export), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def remove_questions_by_ids_v2(ids: set[str]) -> list[dict]:
    """Remove question blocks from category files; return removed question dicts."""
    removed: list[dict] = []

    for path in sorted(CATEGORIES_DIR.glob("*.md")):
        if path.name not in FILE_TO_CATEGORY:
            continue

        content = path.read_text(encoding="utf-8")
        slug, label = FILE_TO_CATEGORY[path.name]
        out_parts: list[str] = []
        cursor = 0
        file_changed = False

        for match in FM_BLOCK_PATTERN.finditer(content):
            meta = yaml.safe_load(match.group(1))
            if not isinstance(meta, dict) or "id" not in meta:
                continue

            qid = meta["id"]
            block_start = match.start()
            body = content[match.end() :]
            nxt = FM_BLOCK_PATTERN.search(body)
            block_end = match.end() + (nxt.start() if nxt else len(body))

            if qid in ids:
                file_changed = True
                body_lines = body[: nxt.start()].splitlines() if nxt else body.splitlines()
                trimmed: list[str] = []
                for line in body_lines:
                    if line.startswith("## "):
                        break
                    trimmed.append(line)
                base = normalize_frontmatter(meta, slug, label, path.name)
                text, options, scale = parse_options(trimmed)
                base["text"] = text
                base["options"] = options
                base["scale"] = scale
                base["reject_reason"] = "intimate_dyadic"
                removed.append(base)
                out_parts.append(content[cursor:block_start])
                cursor = block_end
            else:
                pass

        if file_changed:
            out_parts.append(content[cursor:])
            new_content = "".join(out_parts)
            new_content = re.sub(r"\n{3,}", "\n\n", new_content)
            path.write_text(new_content.rstrip() + "\n", encoding="utf-8")

    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Question Builder")
    parser.add_argument("--dry-run", action="store_true", help="Do not write uid back to md")
    parser.add_argument("--no-write-uid", action="store_true", help="Skip uid writeback")
    parser.add_argument("--include-deprecated", action="store_true", help="Include deprecated in questions.json")
    parser.add_argument("--audit-dyadic", action="store_true", help="Print dyadic audit and exit")
    parser.add_argument("--prune-dyadic", action="store_true", help="Move dyadic questions to rejected/")
    args = parser.parse_args()

    if args.prune_dyadic:
        questions = load_all_questions()
        hits = audit_dyadic(questions)
        ids = {h["id"] for h in hits}
        if not ids:
            print("No dyadic candidates found.")
            return 0
        removed = remove_questions_by_ids_v2(ids)
        append_to_system_unaskable(removed)
        print(f"Pruned {len(removed)} dyadic question(s) → rejected/system_unaskable.md")
        if not args.no_write_uid:
            n = write_uids_to_files(dry_run=args.dry_run)
            if n:
                print(f"Wrote {n} uid(s) to categories")
        questions = load_all_questions()
        write_outputs(questions, args.include_deprecated)
        print(f"Wrote {len([q for q in questions if q['status'] in ('active','candidate')])} active question(s)")
        return 0

    if not args.no_write_uid:
        n = write_uids_to_files(dry_run=args.dry_run)
        if n:
            print(f"Wrote {n} uid(s) to categories")

    questions = load_all_questions()

    if args.audit_dyadic:
        hits = audit_dyadic(questions)
        print(json.dumps(hits, ensure_ascii=False, indent=2))
        print(f"\n{len(hits)} dyadic candidate(s)", file=sys.stderr)
        return 0

    write_outputs(questions, args.include_deprecated)
    active = len([q for q in questions if q["status"] in ("active", "candidate")])
    print(f"Wrote {active} question(s) to {GENERATED_DIR / 'questions.json'}")
    print(f"Wrote stats → {GENERATED_DIR / 'stats.json'}")
    print(f"Wrote duplicate_hints → {GENERATED_DIR / 'duplicate_hints.json'}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
