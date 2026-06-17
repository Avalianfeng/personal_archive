#!/usr/bin/env python3
"""Detect manual edits to sync-generated categories/*.md."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from paths import CATEGORIES_DIR, GENERATED_DIR, FILE_TO_CATEGORY  # noqa: E402

POISON_MARKER = "禁止手动编辑"


def main() -> int:
    manifest_path = GENERATED_DIR / ".sync_manifest.json"
    if not manifest_path.exists():
        print("No sync manifest; run sync_categories first", file=sys.stderr)
        return 1

    doc = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = []
    for fn in FILE_TO_CATEGORY:
        path = CATEGORIES_DIR / fn
        if not path.exists():
            errors.append(f"missing {fn}")
            continue
        text = path.read_text(encoding="utf-8")
        if POISON_MARKER not in text:
            errors.append(f"{fn}: missing poison-pill header (manual edit?)")
        expected = doc.get("files", {}).get(fn)
        if expected:
            actual = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if actual != expected:
                errors.append(f"{fn}: content hash differs from manifest")

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print("categories 为 sync 视图，请用 qcli edit", file=sys.stderr)
        return 1
    print("categories check OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
