# scripts/

| 脚本 | 用途 |
| --- | --- |
| `db.py` | 连接、write 内核、audit（qcli/ingest 共用） |
| `init_db.py` | 建库 |
| `migrate_bootstrap.py` | 一次性迁移（默认 categories） |
| `ingest.py` | 批量写入 imports 队列 |
| `sync_categories.py` | DB → categories/*.md |
| `export_json.py` | → generated/questions.json · stats.json |
| `duplicate_scan.py` | Levenshtein + Jaccard 查重报告 |
| `manage.py` | `sync` / `check` 编排 |
| `check_categories.py` | 检测 categories 手改（pre-commit 可选） |
| `parse_questions.py` | → export_json 薄 wrapper |
| `archive/build_questions.py` | 旧 Markdown 编译链（归档） |

日常操作请用 [`../qcli.py`](../qcli.py)。
