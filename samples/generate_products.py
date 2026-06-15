#!/usr/bin/env python3
"""
从 L1 分析 (samples/report-v1.md) 生成产物 A / B。

用法:
  python samples/generate_products.py a
  python samples/generate_products.py b
  python samples/generate_products.py both

环境:
  .env 中 DEEPSEEK_API_KEY=sk-...
  可选 --provider openai --model gpt-4o
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.llm_client import DEFAULT_DEEPSEEK_MODEL, chat  # noqa: E402

ANALYSIS = ROOT / "samples" / "report-v1.md"
PROMPT_A = ROOT / "prompts" / "product-a-from-l1.md"
PROMPT_B = ROOT / "prompts" / "product-b-from-l1.md"
CATALOG_A = ROOT / "design" / "分析报告目录.md"
CATALOG_B_CORE = ROOT / "design" / "核心档案目录.md"
CATALOG_B_SNAP = ROOT / "design" / "时期快照目录.md"
OUT_A = ROOT / "samples" / "analysis-report-v1.md"
OUT_B = ROOT / "samples" / "person-archive-v1.md"

SECTION_CORE = "---SECTION:核心档案---"
SECTION_SNAP = "---SECTION:时期快照---"
SECTION_CORE_HEADING = "# 核心档案（稳定层）"
SECTION_SNAP_HEADING = "# 时期快照（动态层）"


def catalog_b_combined() -> str:
    core = CATALOG_B_CORE.read_text(encoding="utf-8")
    snap = CATALOG_B_SNAP.read_text(encoding="utf-8")
    return (
        f"### 区块一:核心档案(稳定层)\n\n{core}\n\n"
        f"### 区块二:时期快照(动态层)\n\n{snap}"
    )


def build(prompt_path: Path, analysis: str) -> tuple[str, str]:
    text = prompt_path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SystemExit(f"{prompt_path}: need --- separators")

    system = parts[1].strip()
    user = parts[2].strip()
    system = system.replace("{CATALOG_A}", CATALOG_A.read_text(encoding="utf-8"))
    system = system.replace("{CATALOG_B}", catalog_b_combined())
    user = user.replace("{ANALYSIS_CONTENT}", analysis)
    return system, user


def merge_archive_b(content: str) -> str:
    if SECTION_CORE not in content or SECTION_SNAP not in content:
        preview = content[:500].replace("\n", " ")
        raise SystemExit(
            f"产物 B 响应缺少分隔符 {SECTION_CORE!r} / {SECTION_SNAP!r}。"
            f"响应开头: {preview}…"
        )
    before_snap, snap_body = content.split(SECTION_SNAP, 1)
    core_body = before_snap.split(SECTION_CORE, 1)[1].strip()
    snap_body = snap_body.strip()
    return (
        f"{SECTION_CORE_HEADING}\n\n{core_body}\n\n"
        f"------\n\n"
        f"{SECTION_SNAP_HEADING}\n\n{snap_body}"
    )


def run_one(
    which: str,
    analysis: str,
    model: str,
    provider: str,
    temperature: float,
    dry_run: bool,
) -> None:
    today = date.today().isoformat()

    if which == "a":
        prompt_path = PROMPT_A
        label = "产物 A · 分析报告"
        dry_out = OUT_A.with_name(OUT_A.stem + f"-prompt-{today}.md")
    else:
        prompt_path = PROMPT_B
        label = "产物 B · 人物档案"
        dry_out = OUT_B.with_name(OUT_B.stem + f"-prompt-{today}.md")

    system, user = build(prompt_path, analysis)

    if dry_run:
        dry_out.write_text(
            f"# dry-run · {label}\n\n## system\n\n{system}\n\n## user\n\n{user}",
            encoding="utf-8",
        )
        print(f"[dry-run] {dry_out}")
        return

    print(f"Generating {label} via {provider}/{model} …")
    content = chat(system, user, model, provider=provider, temperature=temperature)

    if which == "a":
        header = f"> {label} · model: {model} · date: {today} · source: report-v1.md\n\n"
        OUT_A.write_text(header + content, encoding="utf-8")
        print(f"Wrote {OUT_A}")
        return

    body = merge_archive_b(content)
    header = f"> {label} · model: {model} · date: {today} · source: report-v1.md\n\n"
    OUT_B.write_text(header + body, encoding="utf-8")
    print(f"Wrote {OUT_B}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "product",
        choices=["a", "b", "both"],
        help="a=分析报告, b=人物档案(单文件双区块), both=依次生成",
    )
    parser.add_argument("--model", default=DEFAULT_DEEPSEEK_MODEL)
    parser.add_argument("--provider", default="deepseek", choices=["deepseek", "openai"])
    parser.add_argument("--temperature", type=float, default=0.5)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not ANALYSIS.exists():
        raise SystemExit(f"Missing {ANALYSIS}")

    analysis = ANALYSIS.read_text(encoding="utf-8")
    targets = ["a", "b"] if args.product == "both" else [args.product]

    for t in targets:
        run_one(t, analysis, args.model, args.provider, args.temperature, args.dry_run)


if __name__ == "__main__":
    main()
