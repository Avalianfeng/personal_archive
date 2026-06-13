#!/usr/bin/env python3
"""Run full-report A/B experiment via DeepSeek API."""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

try:
    import urllib.request
    import json
except ImportError:
    pass

ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = ROOT / "prompts" / "full-report-v1.md"
INTAKE_FULL = ROOT / "samples" / "intake-v1.md"
INTAKE_CLEAN = ROOT / "samples" / "intake-v1-clean.md"
CATALOG = ROOT / "02-档案目录.md"
OUT_DIR = ROOT / "experiments"

API_URL = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-v4-pro"


def load_env() -> None:
    for p in (ROOT / ".env", ROOT / "experiments" / ".env"):
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def catalog_summary() -> str:
    text = CATALOG.read_text(encoding="utf-8")
    # Keep principles + section headers only (rough trim for token budget)
    lines = []
    for line in text.splitlines():
        if line.startswith("#") or line.startswith("## ") or line.startswith("|") and "§" in line:
            lines.append(line)
        if line.startswith("1. **档案是关于人的"):
            lines.append(line)
    return "\n".join(lines[:120]) + "\n\n(完整目录见 02-档案目录.md)"


def build_prompt(variant: str) -> tuple[str, str]:
    template = PROMPT_PATH.read_text(encoding="utf-8")
    if variant == "A":
        intake = INTAKE_CLEAN.read_text(encoding="utf-8")
        mode = "版本 A(纯答案) — 输入已去除所有 {} 与 <<>> 批注"
    else:
        intake = INTAKE_FULL.read_text(encoding="utf-8")
        mode = "版本 B(答案+元认知) — 含 {} 产品批注与 <<>> 旁白,须区分自述与元认知"

    parts = template.split("---", 2)
    if len(parts) < 3:
        raise SystemExit("prompt template must have --- separators")

    system_block = parts[1].strip()
    user_block = parts[2].strip()

    system_block = system_block.replace("{INPUT_MODE}", mode)
    user_block = user_block.replace("{CATALOG_SUMMARY}", catalog_summary())
    user_block = user_block.replace("{INTAKE_CONTENT}", intake)

    return system_block, user_block


def call_deepseek(system: str, user: str, model: str) -> str:
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        raise SystemExit(
            "DEEPSEEK_API_KEY not set. Add to .env or experiments/.env"
        )

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.4,
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=["A", "B"], required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--dry-run", action="store_true", help="Write prompt only, no API")
    args = parser.parse_args()

    load_env()

    if args.variant == "A" and not INTAKE_CLEAN.exists():
        import subprocess

        subprocess.check_call([sys.executable, str(ROOT / "experiments" / "make_intake_clean.py")])

    system, user = build_prompt(args.variant)
    today = date.today().isoformat()
    out_path = OUT_DIR / f"report-v1-{args.variant}-{today}.md"

    if args.dry_run:
        out_path = OUT_DIR / f"prompt-v1-{args.variant}-{today}.md"
        out_path.write_text(
            f"# Prompt dry-run · variant {args.variant}\n\n## System\n\n{system}\n\n## User\n\n{user}",
            encoding="utf-8",
        )
        print(f"Dry-run wrote {out_path} ({len(system)+len(user)} chars)")
        return

    print(f"Calling DeepSeek ({args.model}) variant {args.variant}…")
    content = call_deepseek(system, user, args.model)
    header = f"> Generated: variant {args.variant} · model {args.model} · {today}\n\n"
    out_path.write_text(header + content, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
