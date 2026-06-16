#!/usr/bin/env python3
"""Thin wrapper — use build_questions.py for full pipeline."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_questions import main

if __name__ == "__main__":
    sys.exit(main())
