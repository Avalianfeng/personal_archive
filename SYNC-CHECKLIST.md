# 项目同步检查清单

> **每个新开的 Agent 必须先读本文件。**  
> 宪法：[01-立意与分析体系.md](01-立意与分析体系.md)

---

## 新 Agent 启动顺序

1. 本文件（SYNC-CHECKLIST.md）
2. [01-立意与分析体系.md](01-立意与分析体系.md)
3. [项目状态.md](项目状态.md)
4. [questions/README.md](questions/README.md) — 知识层入口
5. 若动题库：[整理规范-v1.0.md](questions/整理规范-v1.0.md) · [question_registry/schema.sql](questions/question_registry/schema.sql)

---

## 核心文件（会话开始确认是否过期）

- [ ] [01-立意与分析体系.md](01-立意与分析体系.md)
- [ ] [02-维度地图-dimensions.md](02-维度地图-dimensions.md)
- [ ] [项目状态.md](项目状态.md)
- [ ] [README.md](README.md)
- [ ] [design/00-档案文件群-index.md](design/00-档案文件群-index.md)
- [ ] [questions/README.md](questions/README.md)
- [ ] [questions/question_registry/schema.sql](questions/question_registry/schema.sql)
- [ ] [questions/registries/*.yaml](questions/registries/)

---

## 触发规则

| 你改了什么 | 必须同步检查 |
| --- | --- |
| 宪法（01） | **全部**下游 |
| 维度地图（02）§14 | catalog · questions · persona |
| 文件群结构 | 01 §3 · 02 §14 · 00-index · 项目状态 · README |
| `question_registry/schema.sql` | scripts · schema/格式规范 · qcli · ingest |
| `registries/*.yaml` | ingest 校验 · qcli registry · 整理/审查提示词 |
| ingest 契约 | 问题整理提示词 · 整理规范 v1.0 |
| qcli 子命令 | questions/README · 审查提示词 |
| source_library 卡片 | 只更新路径，不写 DB |
| sync_categories 模板 | categories/README · check_categories |

---

## 架构速记（questions 子系统）

| 概念 | 当前 | 已废止 |
| --- | --- | --- |
| 项目性质 | 人物档案引擎**知识层** | 问卷/题库软件 |
| Level 1 | `source_library/`（不导入 DB） | question_sources → DB |
| Level 2 存储 | `question_registry/questions.db` | categories frontmatter 手改 |
| 认知导航 | `categories/`（sync 视图） | 手改 md 为真源 |
| 规则 | `registries/*.yaml` only | registries/*.md |
| 操纵 | `questions/qcli.py` | 开 md 改题 |
| 收件箱 | `imports/` → ingest | raw/ 主流程 |
| 审计 | `generated/` + export 捆绑 | duplicates/ 手改 |
| 编译 | export_json · sync_categories | build_questions.py（归档） |

### 写操作契约

DB 写入 → audit.log → **sync_categories** → **export_json**

---

## 归档参考

[archive/reference/README.md](archive/reference/README.md)
