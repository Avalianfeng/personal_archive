#!/usr/bin/env python3
"""Same intake + same L1 prompt → multiple models → compare outputs."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.llm_client import DEFAULT_DEEPSEEK_MODELS, chat, model_slug  # noqa: E402

PROMPT_PATH = ROOT / "archive" / "reference" / "l1-analysis-v1.md"
INTAKE = ROOT / "samples" / "intake-v1-clean.md"
CATALOG = ROOT / "02-维度地图-dimensions.md"
OUT_DIR = ROOT / "experiments" / "outputs"

def catalog_summary() -> str:
    lines = []
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or (line.startswith("|") and "§" in line):
            lines.append(line)
        if line.startswith("1. **档案是关于人的"):
            lines.append(line)
    return "\n".join(lines[:100])


def build_messages() -> tuple[str, str]:
    template = PROMPT_PATH.read_text(encoding="utf-8")
    parts = template.split("---", 2)
    if len(parts) < 3:
        raise SystemExit("prompt must have --- separators (system / user)")

    system = parts[1].strip()
    user = parts[2].strip()
    user = user.replace("{CATALOG_SUMMARY}", catalog_summary())
    user = user.replace("{INTAKE_CONTENT}", INTAKE.read_text(encoding="utf-8"))
    return system, user


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-model L1 analysis compare")
    parser.add_argument(
        "--models",
        default=",".join(DEFAULT_DEEPSEEK_MODELS),
        help="Comma-separated model ids",
    )
    parser.add_argument("--provider", default="deepseek", choices=["deepseek", "openai"])
    parser.add_argument("--temperature", type=float, default=0.4)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not INTAKE.exists():
        raise SystemExit(f"Missing {INTAKE} — run archive script or copy from samples")

    system, user = build_messages()
    today = date.today().isoformat()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    for model in models:
        slug = model_slug(model)
        out = OUT_DIR / f"l1-{slug}-{today}.md"

        if args.dry_run:
            out = OUT_DIR / f"prompt-{slug}-{today}.md"
            out.write_text(
                f"# dry-run · {model}\n\n## system\n\n{system}\n\n## user\n\n{user}",
                encoding="utf-8",
            )
            print(f"[dry-run] {out}")
            continue

        print(f"Calling {args.provider}/{model} …")
        content = chat(system, user, model, provider=args.provider, temperature=args.temperature)
        header = f"> model: {model} · provider: {args.provider} · date: {today}\n\n"
        out.write_text(header + content, encoding="utf-8")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
