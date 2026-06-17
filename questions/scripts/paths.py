"""Shared paths and constants for questions subsystem."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
QUESTIONS_DIR = REPO_ROOT / "questions"
REGISTRY_DIR = QUESTIONS_DIR / "question_registry"
DB_PATH = REGISTRY_DIR / "questions.db"
SCHEMA_PATH = REGISTRY_DIR / "schema.sql"
CATEGORIES_DIR = QUESTIONS_DIR / "categories"
GENERATED_DIR = QUESTIONS_DIR / "generated"
REGISTRIES_DIR = QUESTIONS_DIR / "registries"
SOURCE_LIBRARY_DIR = QUESTIONS_DIR / "source_library"
IMPORTS_DIR = QUESTIONS_DIR / "imports"
IMPORTS_PENDING = IMPORTS_DIR / "pending"
IMPORTS_PROCESSED = IMPORTS_DIR / "processed"
IMPORTS_FAILED = IMPORTS_DIR / "failed"
IMPORTS_EXTERNAL = IMPORTS_DIR / "external"
REJECTED_DIR = QUESTIONS_DIR / "rejected"
SCRIPTS_DIR = QUESTIONS_DIR / "scripts"
QCLI_PATH = QUESTIONS_DIR / "qcli.py"

ALLOWED_INGEST_ROOTS = (
    IMPORTS_PENDING,
    IMPORTS_EXTERNAL,
)

FORBIDDEN_INGEST_ROOTS = (
    SOURCE_LIBRARY_DIR,
    CATEGORIES_DIR,
    REGISTRIES_DIR,
    REJECTED_DIR,
)

IGNORE_EXTENSIONS = {".pdf", ".js", ".ts", ".png", ".jpg", ".zip"}

FILE_TO_CATEGORY: dict[str, tuple[str, str]] = {
    "现实问题.md": ("real", "现实问题"),
    "情感问题.md": ("emo", "情感问题"),
    "决策问题.md": ("dec", "决策问题"),
    "状态问题.md": ("sta", "状态问题"),
    "自我认知.md": ("self", "自我认知"),
    "价值问题.md": ("val", "价值问题"),
    "其他.md": ("oth", "其他"),
}

CATEGORY_FILES = [name for name in FILE_TO_CATEGORY if name != "README.md"]
