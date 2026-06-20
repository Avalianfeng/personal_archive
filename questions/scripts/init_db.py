#!/usr/bin/env python3
"""Initialize 04-存储层-Store/questions.db from schema.sql."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import init_database, set_meta, utc_now  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize questions database")
    parser.add_argument("--force", action="store_true", help="Drop and recreate database")
    args = parser.parse_args()
    path = init_database(force=args.force)
    set_meta("initialized_at", utc_now())
    print(f"Database ready: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
