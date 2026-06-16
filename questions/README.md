# questions/ · 人物建档问题库

> **规范**：[整理规范-v0.1.md](./整理规范-v0.1.md) · [schema/格式规范.md](./schema/格式规范.md) v0.4

---

## 数据流

```text
question_sources/     来源档案馆（`[状态][Px]` 前缀，卡片不移动）
raw/pending/          待整理（`[Px]` / `[批次]` / `[元]` 前缀）
      ↓ 整理 Agent
categories/*.md       人类编辑（uid + frontmatter）
registries/*.yaml     prerequisites / tags 标准库
      ↓ build_questions.py
generated/*.json      程序产物（gitignore）
      ↓ 查重
duplicates/
      ↓ raw 移入
raw/processed/
rejected/             文件级 + system_unaskable 单题
```

---

## 关键概念

| 概念 | 说明 |
| --- | --- |
| `uid` | 主键（8 hex）；Builder 自动补 |
| `id` | 人类编号；**删题不重排** |
| `prerequisites` | 语义严格前提（无此事实则问题不成立）→ [registries/prerequisites.yaml](./registries/prerequisites.yaml) |
| `tags` | 主题检索（关于什么）→ [registries/tags.yaml](./registries/tags.yaml) |
| `system_unaskable` | 二元对话题 → rejected，不入 categories |
| pending/processed | raw 处理队列 |

**边界**：`question_guides/` · `analysis_guides/` 本阶段不做；解读靠运行时 AI + 资料。

---

## 目录

| 目录 | 职责 |
| --- | --- |
| `schema/` | 格式规范 + JSON Schema |
| `registries/` | prerequisites / tags 标准库 |
| `scripts/` | `build_questions.py` |
| `generated/` | 编译产物（含 `registries.json` 快照） |
| `categories/` | 问题地图（209 题，StoryCorps P1 后） |
| `raw/pending/` · `raw/processed/` | 原始材料队列（见 [raw/README.md](./raw/README.md) 前缀规范） |
| `rejected/` | 淘汰 |
| `duplicates/` | 查重报告 |
| `question_sources/` | 来源索引（`[状态][Px]` 文件名前缀） |
| `canonical/` · `bank/` | 远期 / 500+ 题后 |

整理 Agent **禁止读 02**。

---

## 命令

```bash
python questions/scripts/build_questions.py
python questions/scripts/build_questions.py --audit-dyadic
python questions/scripts/build_questions.py --strict-registry
```

Agent：[问题整理提示词.md](./prompts/问题整理提示词.md) · [问题查重提示词.md](./prompts/问题查重提示词.md) · [registry审核提示词.md](./prompts/registry审核提示词.md)

整理批次验收：[整理规范-v0.1.md §二十一](./整理规范-v0.1.md)
