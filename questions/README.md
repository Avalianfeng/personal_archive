# questions/ · 人物档案引擎 · 知识层

> **不是问卷系统** — Level 1 文献馆 + Level 2 题目仓库 + Registry 规则 + categories 导航 + qcli 操纵层。

## 唯一入口

| 你是谁 | 命令 |
| --- | --- |
| **日常维护** | `python questions/qcli.py ...` |
| **CI / 全量刷新** | `python questions/scripts/manage.py sync` |
| **健康检查** | `python questions/qcli.py doctor` |
| **一次性迁移** | `python questions/scripts/migrate_bootstrap.py --from-categories` |
| **开发者** | 只 import `questions/scripts/db.py` |

依赖：`pip install -r requirements.txt`（Windows 推荐 Windows Terminal / Git Bash）

## 目录

| 目录 | 层级 | 职责 |
| --- | --- | --- |
| `source_library/` | Level 1 | 协议/方法论文献馆 — **永不 bulk 导入 DB** |
| `question_registry/` | Level 2 | `questions.db` + `schema.sql` |
| `categories/` | 表现层 | 问题地图（sync 生成，**禁止手改**） |
| `registries/` | 规则层 | 仅 `*.yaml` 真源 |
| `imports/` | 收件箱 | jsonl → `ingest.py` |
| `generated/` | 审计层 | json/stats/查重/audit（部分 json 入 Git） |
| `qcli.py` | 操纵层 | 浏览/编辑/审查 |
| `prompts/` | Agent | 整理/查重/审查 |
| `rejected/` | 来源淘汰 | 不进 DB |

## 数据流

```text
source_library → Agent 提炼 → imports/pending → ingest.py → question_registry.db
                                                              ↓
                    qcli.py ← sync_categories → categories/*.md
                          ← export_json / duplicate_scan → generated/
```

## 写操作契约

任何写入 DB：`校验 registries → WRITE → audit.log → sync_categories → export_json`

## 常用命令

```bash
python questions/qcli.py list --category real --limit 20
python questions/qcli.py show Q-REAL-042
python questions/qcli.py edit Q-REAL-042 --set subcategory=家庭与成长
python questions/qcli.py review --batch 10 --session review_20260616
python questions/qcli.py registry list tags
python questions/scripts/ingest.py
python questions/scripts/manage.py sync --ingest
```

Bootstrap（新 clone）：

```bash
pip install -r requirements.txt
python questions/scripts/init_db.py
python questions/scripts/migrate_bootstrap.py
python questions/scripts/sync_categories.py
python questions/scripts/export_json.py
```

规范：[整理规范-v1.0.md](./整理规范-v1.0.md) · [schema/格式规范.md](./schema/格式规范.md)
