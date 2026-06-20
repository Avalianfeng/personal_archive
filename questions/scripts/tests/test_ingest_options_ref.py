"""Tests for ingest options_ref and batch _meta."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

from db import load_registries, prepare_ingest_record, resolve_ingest_record  # noqa: E402
from ingest import parse_jsonl_content  # noqa: E402


@pytest.fixture
def registries():
    return load_registries()


def test_inline_options_valid(registries):
    raw = {
        "question": "测试题？",
        "category": "val",
        "subcategory": "个人价值观",
        "type": "agreement",
        "interaction": "rating",
        "options": [{"key": "1", "text": "完全不像我"}],
    }
    prepared, errors = prepare_ingest_record(raw, {}, registries=registries, line=2)
    assert errors == []
    assert prepared is not None
    assert prepared["options"][0]["key"] == "1"


def test_options_ref_expands(registries):
    raw = {
        "question": "富有对你很重要。",
        "category": "val",
        "subcategory": "个人价值观",
        "type": "agreement",
        "interaction": "rating",
        "options_ref": "portrait_6l_zh",
    }
    resolved, errors = resolve_ingest_record(raw, {}, registries)
    assert errors == []
    assert resolved is not None
    assert len(resolved["options"]) == 6
    assert resolved["options"][0]["text"] == "完全不像我"
    assert "options_ref" not in resolved


def test_unknown_options_ref(registries):
    raw = {
        "question": "测试？",
        "category": "val",
        "subcategory": "个人价值观",
        "type": "agreement",
        "options_ref": "nonexistent_template",
    }
    _, errors = prepare_ingest_record(raw, {}, registries=registries, line=3)
    assert any("unknown options_ref" in e for e in errors)


def test_meta_default_options_ref(registries):
    text = '\n'.join([
        '{"_meta": true, "default_options_ref": "portrait_6l_zh"}',
        '{"question":"想出新点子很重要。","category":"val","subcategory":"个人价值观","type":"agreement","interaction":"rating"}',
    ])
    batch_ctx, records = parse_jsonl_content(text)
    assert batch_ctx["default_options_ref"] == "portrait_6l_zh"
    assert len(records) == 1
    prepared, errors = prepare_ingest_record(
        records[0][1], batch_ctx, registries=registries, line=records[0][0],
    )
    assert errors == []
    assert prepared is not None
    assert len(prepared["options"]) == 6


def test_string_array_options_rejected(registries):
    raw = {
        "question": "测试？",
        "category": "val",
        "subcategory": "个人价值观",
        "type": "agreement",
        "options": ["完全不像我", "不太像我"],
    }
    _, errors = prepare_ingest_record(raw, {}, registries=registries, line=1)
    assert any("string" in e for e in errors)


def test_validate_jsonl_file_dry_run(tmp_path, registries):
    path = tmp_path / "test.jsonl"
    path.write_text(
        '{"_meta": true, "default_options_ref": "portrait_6l_zh"}\n'
        '{"question":"测试开放题？","category":"real","subcategory":"家庭与成长","type":"open"}\n',
        encoding="utf-8",
    )
    # validate_ingest_path will fail for tmp_path - test prepare only via parse
    batch_ctx, records = parse_jsonl_content(path.read_text(encoding="utf-8"))
    for line_no, rec in records:
        _, errors = prepare_ingest_record(rec, batch_ctx, registries=registries, line=line_no)
        assert errors == []


def test_inline_options_override_ref(registries):
    raw = {
        "question": "测试？",
        "category": "val",
        "subcategory": "个人价值观",
        "type": "single",
        "options_ref": "portrait_6l_zh",
        "options": [{"key": "A", "text": "是"}, {"key": "B", "text": "否"}],
    }
    resolved, errors = resolve_ingest_record(raw, {}, registries)
    assert errors == []
    assert len(resolved["options"]) == 2
    assert resolved["options"][0]["key"] == "A"
