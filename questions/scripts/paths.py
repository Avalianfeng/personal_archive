"""Shared paths and constants for questions subsystem."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
QUESTIONS_DIR = REPO_ROOT / "questions"

LIBRARY_DIR = QUESTIONS_DIR / "01-文献与来源-Library"
VIEWS_DIR = QUESTIONS_DIR / "02-问题地图-Views"
META_DIR = QUESTIONS_DIR / "03-规则与审计-Meta"
STORE_DIR = QUESTIONS_DIR / "04-存储层-Store"
IMPORTS_DIR = QUESTIONS_DIR / "05-导入队列-Imports"
SCRIPTS_DIR = QUESTIONS_DIR / "scripts"

REGISTRIES_DIR = META_DIR / "01-registries-规则真源"
SCHEMA_DIR = META_DIR / "02-schema-格式契约"
GENERATED_DIR = META_DIR / "03-generated-审计产物"
PROMPTS_DIR = META_DIR / "04-prompts-Agent提示"
RULES_PATH = META_DIR / "00-整理规范-v1.0.md"

AGENT_VIEWS_DIR = GENERATED_DIR / "01-agent-Agent视图"
BY_CATEGORY_DIR = AGENT_VIEWS_DIR / "by_category"
REVIEW_SESSIONS_DIR = GENERATED_DIR / "02-review-sessions-审查会话"

REGISTRY_DIR = STORE_DIR
DB_PATH = STORE_DIR / "questions.db"
SCHEMA_PATH = STORE_DIR / "schema.sql"
FORMAT_SPEC_PATH = SCHEMA_DIR / "01-格式规范.md"

CATEGORIES_DIR = VIEWS_DIR
SOURCE_LIBRARY_DIR = LIBRARY_DIR
REJECTED_DIR = LIBRARY_DIR / "96-rejected-淘汰池"
LIBRARY_META_DIR = LIBRARY_DIR / "97-meta-元数据"
LIBRARY_ARCHIVE_DIR = LIBRARY_DIR / "98-archive-归档"

IMPORTS_PENDING = IMPORTS_DIR / "01-pending-待入库"
IMPORTS_PROCESSED = IMPORTS_DIR / "02-processed-已入库"
IMPORTS_FAILED = IMPORTS_DIR / "03-failed-失败"
IMPORTS_EXTERNAL = IMPORTS_DIR / "04-external-外部工具"

SCRIPTS_ARCHIVE_DIR = SCRIPTS_DIR / "99-archive-历史"
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

# Agent 提示词（有序）
PROMPT_FILES = {
    "ingest_agent": PROMPTS_DIR / "01-整理Agent启动.md",
    "ingest_prompt": PROMPTS_DIR / "02-问题整理提示词.md",
    "taxonomy": PROMPTS_DIR / "03-分类原则.md",
    "cleanup_agent": PROMPTS_DIR / "04-清理期Agent启动.md",
    "dedup_prompt": PROMPTS_DIR / "05-问题查重提示词.md",
    "review_prompt": PROMPTS_DIR / "06-问题审查提示词.md",
    "registry_prompt": PROMPTS_DIR / "07-registry审核提示词.md",
}
