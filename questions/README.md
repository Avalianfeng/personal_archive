# questions/ · 人物档案引擎 · 知识层

> **不是问卷系统** — 生命周期分层 + qcli 操纵层。

## 顶层导航

| 序号 | 目录 | 职责 |
| --- | --- | --- |
| — | 本文件 · `qcli.py` · `requirements.txt` | 入口 |
| 01 | [文献与来源-Library/](./01-文献与来源-Library/README.md) | 源料（只读） |
| 02 | [问题地图-Views/](./02-问题地图-Views/README.md) | sync 视图 |
| 03 | [规则与审计-Meta/](./03-规则与审计-Meta/README.md) | 规范 · 提示词 · 审计 |
| 04 | [存储层-Store/](./04-存储层-Store/README.md) | SQLite |
| 05 | [导入队列-Imports/](./05-导入队列-Imports/README.md) | jsonl 队列 |
| — | [scripts/](./scripts/README.md) | 运维脚本 |

**命名**：顶层 `01`–`05` 有生命周期顺序；并列支撑层（如 `scripts/`）不加序号。子目录同理——有流程则保留序号，纯并列以可读为主。

## Agent 速查

| 角色 | 写入 | 验收 | 读库 |
| --- | --- | --- | --- |
| **整理 Agent** | `05-Imports/01-pending/*.jsonl` | `manage accept --json` | `batch_delta_compact.md` · `batch_delta.json` · `health.json` |
| **维护/查重 Agent** | `qcli edit` / `qcli relate` | `qcli doctor` | `qcli dump` / `dump --batch` / `search` / `show` |

**整理期不要用** `qcli ingest`（缺 `batch_delta` 计算）。**查重期**优先 `qcli search` + `by_category/*.md`，全库 `bank_compact.md` 作 fallback。

可用量表模板：`qcli registry list options_templates` → jsonl 用 `options_ref` 代替逐行 `options`。

## 按角色入口

| 角色 | 第一步 | 常用命令 |
| --- | --- | --- |
| **整理 Agent** | [04-prompts/01-整理Agent启动.md](./03-规则与审计-Meta/04-prompts-Agent提示/01-整理Agent启动.md) | `ingest --dry-run` → `manage accept --json` |
| **维护 Agent** | `03-generated/01-agent-Agent视图/bank_compact.md` | `qcli edit` / `qcli dump` |
| **清理 Agent** | [04-prompts/04-清理期Agent启动.md](./03-规则与审计-Meta/04-prompts-Agent提示/04-清理期Agent启动.md) | `sync --with-duplicate-scan` |
| **健康检查** | — | `qcli doctor` |

## 宏观流程

```text
01-Library → 整理 Agent → 05-Imports/01-pending/*.jsonl
                         → manage accept --json
                         → 04-Store + 03-Meta/03-generated/
                         → 02-Views（sync）
```

Bootstrap：

```bash
pip install -r requirements.txt
python questions/scripts/init_db.py
python questions/scripts/migrate_bootstrap.py
python questions/scripts/manage.py sync
```

规范：[03-Meta/00-整理规范-v1.0.md](./03-规则与审计-Meta/00-整理规范-v1.0.md)
