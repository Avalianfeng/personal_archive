#!/usr/bin/env python3
"""Duplicate scan: Levenshtein ratio + keyword Jaccard → generated reports."""

from __future__ import annotations

import json
import re
import sys
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import fetch_all_questions  # noqa: E402
from paths import GENERATED_DIR  # noqa: E402

THRESHOLD = 0.85
STOPWORDS = {"的", "了", "在", "是", "我", "你", "他", "她", "它", "我们", "你们", "他们", "什么", "怎么", "如何", "吗", "呢", "啊"}


def normalize_text(text: str) -> str:
    t = re.sub(r"\s+", "", text.lower())
    t = re.sub(r"[？?！!。，,、；;：:\"\"''（）()\\[\\]/]", "", t)
    return t


def tokenize(text: str) -> set[str]:
    t = re.sub(r"[？?！!。，,、；;：:\"\"''（）()\\[\\]/\\s]+", " ", text.lower())
    parts = [p for p in t.split() if len(p) >= 2 and p not in STOPWORDS]
    if not parts:
        parts = [p for p in t.split() if p and p not in STOPWORDS]
    return set(parts)


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def similarity(q1: dict, q2: dict) -> tuple[float, str]:
    t1 = normalize_text(q1["text"])
    t2 = normalize_text(q2["text"])
    if t1 == t2:
        return 1.0, "exact_duplicate"
    ratio = SequenceMatcher(None, t1, t2).ratio()
    jac = jaccard(tokenize(q1["text"]), tokenize(q2["text"]))
    score = max(ratio, jac)
    hint = f"编辑距离比率 {ratio:.2f} · 关键词 Jaccard {jac:.2f}"
    if jac >= 0.5:
        hint = f"核心词重叠 {jac:.0%} · {hint}"
    return score, hint


def duplicate_scan(*, active_only: bool = True) -> dict:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    questions = fetch_all_questions()
    if active_only:
        questions = [q for q in questions if q["status"] in ("active", "candidate")]

    exact: dict[str, list[str]] = {}
    for q in questions:
        key = normalize_text(q["text"])
        exact.setdefault(key, []).append(q["id"])
    exact_dups = [
        {"text_normalized": k, "ids": ids}
        for k, ids in exact.items()
        if len(ids) > 1
    ]

    pairs = []
    for q1, q2 in combinations(questions, 2):
        score, hint = similarity(q1, q2)
        if score >= THRESHOLD and q1["id"] != q2["id"]:
            pairs.append({
                "id_a": q1["id"],
                "id_b": q2["id"],
                "similarity_score": round(score, 4),
                "hint": hint,
            })
    pairs.sort(key=lambda x: -x["similarity_score"])

    hints = {"exact_text_duplicates": exact_dups, "count": len(exact_dups), "similar_pairs": pairs}
    (GENERATED_DIR / "duplicate_hints.json").write_text(
        json.dumps({"exact_text_duplicates": exact_dups, "count": len(exact_dups)}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Duplicate Report",
        "",
        f"> Threshold: {THRESHOLD} · Active questions: {len(questions)}",
        "",
        "## Exact duplicates",
        "",
    ]
    if not exact_dups:
        lines.append("_None_")
    else:
        for item in exact_dups:
            lines.append(f"- {', '.join(item['ids'])}")
    lines.extend(["", "## Similar pairs (review via qcli relate)", ""])
    if not pairs:
        lines.append("_None above threshold_")
    else:
        for p in pairs[:200]:
            lines.append(
                f"- {p['id_a']} ↔ {p['id_b']} · score {p['similarity_score']} · {p['hint']}",
            )
    (GENERATED_DIR / "duplicate_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return hints


def main() -> int:
    result = duplicate_scan()
    print(f"Exact duplicate groups: {result['count']}")
    print(f"Report → {GENERATED_DIR / 'duplicate_report.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
