#!/usr/bin/env python3
"""Cross-platform pre-commit checks for questions/ subsystem."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
from paths import IMPORTS_PENDING  # noqa: E402


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=REPO_ROOT)


def pending_jsonl() -> list[Path]:
    if not IMPORTS_PENDING.exists():
        return []
    return sorted(
        p for p in IMPORTS_PENDING.iterdir()
        if p.is_file() and p.suffix.lower() in {".jsonl", ".json"} and p.name != "README.md"
    )


def main() -> int:
    rc = run([sys.executable, "-m", "pytest", str(SCRIPTS / "tests"), "-q"])
    if rc != 0:
        return rc

    rc = run([sys.executable, str(SCRIPTS / "check_categories.py")])
    if rc != 0:
        return rc

    pending = pending_jsonl()
    if pending:
        rel = IMPORTS_PENDING.relative_to(REPO_ROOT).as_posix()
        print(f"[pre-commit] {len(pending)} jsonl in {rel}/ — running dry-run + doctor")
        rc = run([sys.executable, str(SCRIPTS / "ingest.py"), "--dry-run"])
        if rc != 0:
            print("Fix jsonl errors before commit.", file=sys.stderr)
            return rc
        rc = run([sys.executable, str(SCRIPTS / "manage.py"), "check"])
        if rc != 0:
            print("Doctor check failed.", file=sys.stderr)
            return rc
        print("[pre-commit] pending jsonl validated; run `manage accept` when ready to ingest")

    return 0


if __name__ == "__main__":
    sys.exit(main())
