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
sys.path.insert(0, str(ROOT / "experiments"))

from llm_client import chat  # noqa: E402

ANALYSIS = ROOT / "samples" / "report-v1.md"
PROMPT_A = ROOT / "prompts" / "product-a-from-l1.md"
PROMPT_B = ROOT / "prompts" / "product-b-from-l1.md"
CATALOG_A = ROOT / "design" / "分析报告目录.md"
CATALOG_B = ROOT / "design" / "人物档案目录.md"
OUT_A = ROOT / "samples" / "analysis-report-v1.md"
OUT_B = ROOT / "samples" / "person-archive-v1.md"


def build(system_user_template: Path, catalog: Path, analysis: str) -> tuple[str, str]:
    text = system_user_template.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SystemExit(f"{system_user_template}: need --- separators")

    system = parts[1].strip()
    user = parts[2].strip()
    system = system.replace("{CATALOG_A}", catalog.read_text(encoding="utf-8"))
    system = system.replace("{CATALOG_B}", catalog.read_text(encoding="utf-8"))
    user = user.replace("{ANALYSIS_CONTENT}", analysis)
    return system, user


def run_one(
    which: str,
    analysis: str,
    model: str,
    provider: str,
    temperature: float,
    dry_run: bool,
) -> None:
    if which == "a":
        prompt_path, catalog, out = PROMPT_A, CATALOG_A, OUT_A
        label = "产物 A · 分析报告"
    else:
        prompt_path, catalog, out = PROMPT_B, CATALOG_B, OUT_B
        label = "产物 B · 人物档案"

    system, user = build(prompt_path, catalog, analysis)
    today = date.today().isoformat()

    if dry_run:
        out = out.with_name(out.stem + f"-prompt-{today}.md")
        out.write_text(
            f"# dry-run · {label}\n\n## system\n\n{system}\n\n## user\n\n{user}",
            encoding="utf-8",
        )
        print(f"[dry-run] {out}")
        return

    print(f"Generating {label} via {provider}/{model} …")
    content = chat(system, user, model, provider=provider, temperature=temperature)
    header = f"> {label} · model: {model} · date: {today} · source: report-v1.md\n\n"
    out.write_text(header + content, encoding="utf-8")
    print(f"Wrote {out}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "product",
        choices=["a", "b", "both"],
        help="a=分析报告, b=人物档案, both=依次生成",
    )
    parser.add_argument("--model", default="deepseek-chat")
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
