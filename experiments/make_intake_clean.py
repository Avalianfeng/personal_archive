#!/usr/bin/env python3
"""Derive samples/intake-v1-clean.md from frozen intake-v1.md (answers only)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "samples" / "intake-v1.md"
DST = ROOT / "samples" / "intake-v1-clean.md"


def strip_inline_braces(line: str) -> str:
    """Remove inline {…} and <<…>> segments, keep surrounding text."""
    line = re.sub(r"\{[^{}]*\}", "", line)
    line = re.sub(r"<<[^>]*>>", "", line)
    return line


def strip_annotations(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    in_brace = False
    in_angle = False

    for line in lines:
        stripped = line.strip()

        if in_brace:
            if "}" in line:
                in_brace = False
                rest = line.split("}", 1)[1]
                if rest.strip():
                    out.append(rest)
            continue

        if in_angle:
            if ">>" in line:
                in_angle = False
                rest = line.split(">>", 1)[1]
                if rest.strip():
                    out.append(rest)
            continue

        if stripped.startswith("{") and "}" not in line:
            in_brace = True
            continue
        if stripped.startswith("{") and stripped.endswith("}"):
            continue
        if "{" in line or "<<" in line:
            cleaned = strip_inline_braces(line)
            if cleaned.strip():
                out.append(cleaned)
            continue

        # Drop meta lines about annotation conventions (product doc, not answers)
        if stripped.startswith('> "{}') or stripped.startswith('> “{}”'):
            continue
        if stripped.startswith('> “<<>>”') or stripped.startswith('> "<<"'):
            continue

        out.append(line)

    # Collapse excessive blank lines
    result = "".join(out)
    while "\n\n\n\n" in result:
        result = result.replace("\n\n\n\n", "\n\n\n")
    return result


def patch_header(text: str) -> str:
    text = text.replace(
        "../archive-catalog-v1.md",
        "../02-档案目录.md",
    )
    header = """# 人物档案建档问卷 V1 · 纯答案版

> **来源**:由 [intake-v1.md](./intake-v1.md) 自动导出。已去除 `{}` 产品批注与 `<<>>` 个人旁白,**只保留题目与答案**。
> **用途**:实验 A(版本 1 输入)、贫语料分析基线。原卷冻结不改,本文件可随导出脚本重生成。

---

"""
    # Skip original title + product positioning through first ---
    idx = text.find("\n---\n\n## 填写前")
    if idx == -1:
        idx = text.find("\n---\n\n# 第零部分")
    body = text[idx + len("\n---\n\n") :] if idx != -1 else text
    if body.startswith("## 填写前"):
        pass
    elif body.startswith("# 第零部分"):
        body = "## 填写前\n\n**你在建立自己的档案,不是在参加测试。**\n\n---\n\n" + body
    return header + body


def main() -> None:
    raw = SRC.read_text(encoding="utf-8")
    clean = patch_header(strip_annotations(raw))
    DST.write_text(clean, encoding="utf-8")
    print(f"Wrote {DST} ({len(clean.splitlines())} lines)")


if __name__ == "__main__":
    main()
