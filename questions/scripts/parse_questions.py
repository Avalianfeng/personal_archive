#!/usr/bin/env python3
"""Compile categories/*.md (YAML frontmatter blocks) to generated/questions.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

QUESTIONS_DIR = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = QUESTIONS_DIR / "categories"
OUTPUT_PATH = QUESTIONS_DIR / "generated" / "questions.json"

FILE_TO_CATEGORY: dict[str, tuple[str, str]] = {
    "现实问题.md": ("real", "现实问题"),
    "情感问题.md": ("emo", "情感问题"),
    "决策问题.md": ("dec", "决策问题"),
    "状态问题.md": ("sta", "状态问题"),
    "自我认知.md": ("self", "自我认知"),
    "价值问题.md": ("val", "价值问题"),
    "其他.md": ("oth", "其他"),
}

VALID_TYPES = {"open", "single", "multi", "scale", "sort", "fill", "agreement"}
VALID_INTERACTIONS = {
    "story",
    "self_report",
    "scenario",
    "comparison",
    "rating",
    "reflection",
    "future",
}
VALID_STATUS = {"active", "candidate", "deprecated"}
VALID_DEPTH = {"shallow", "medium", "deep"}
ID_PATTERN = re.compile(r"^Q-(REAL|EMO|DEC|STA|SELF|VAL|OTH)-\d{3}$")
OPTION_PATTERN = re.compile(r"^-\s*([A-Z])\.\s*(.+)$")
FM_BLOCK_PATTERN = re.compile(r"(?ms)^---\s*\n(.*?)\n---\s*\n")


def empty_to_none(value):
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


def parse_options(body_lines: list[str]) -> tuple[str, list[dict[str, str]] | None, str | None]:
    """Return (question_text, options, scale_note)."""
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
        "superseded_by": empty_to_none(meta.get("superseded_by")),
        "deprecated_reason": empty_to_none(meta.get("deprecated_reason")),
        "source_file": source_file,
    }


def parse_category_file(path: Path) -> list[dict]:
    if path.name not in FILE_TO_CATEGORY:
        return []

    slug, label = FILE_TO_CATEGORY[path.name]
    content = path.read_text(encoding="utf-8")
    questions: list[dict] = []

    for match in FM_BLOCK_PATTERN.finditer(content):
        meta = yaml.safe_load(match.group(1))
        if not isinstance(meta, dict) or "id" not in meta:
            continue

        body = content[match.end() :]
        next_fm = FM_BLOCK_PATTERN.search(body)
        body_text = body[: next_fm.start()] if next_fm else body
        body_lines = body_text.splitlines()

        base = normalize_frontmatter(meta, slug, label, path.name)
        text, options, scale = parse_options(body_lines)

        if not text:
            raise ValueError(f"{path.name} {base['id']}: empty question text")

        base["text"] = text
        base["options"] = options
        base["scale"] = scale
        questions.append(base)

    return questions


def main() -> int:
    all_questions: list[dict] = []
    seen_ids: set[str] = set()

    for path in sorted(CATEGORIES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        for q in parse_category_file(path):
            if q["id"] in seen_ids:
                print(f"Error: duplicate id {q['id']}", file=sys.stderr)
                return 1
            seen_ids.add(q["id"])
            all_questions.append(q)

    all_questions.sort(key=lambda q: q["id"])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(all_questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(all_questions)} question(s) to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
