#!/usr/bin/env python3
"""Thin wrapper — delegates to export_json.py (legacy entry point)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_json import main

if __name__ == "__main__":
    sys.exit(main())
