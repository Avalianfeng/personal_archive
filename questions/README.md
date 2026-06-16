# questions/ · 人物建档问题库

> **整理规范**：[整理规范-v0.1.md](./整理规范-v0.1.md) · **格式契约**：[schema/格式规范.md](./schema/格式规范.md) v0.2
> **关联**：[02-维度地图](../02-维度地图-dimensions.md)（**整理 Agent 禁止读取**）

---

## 数据流

```text
question_sources/  →  raw/
         ↓ 整理 Agent
      categories/*.md     ← 人类编辑（YAML frontmatter）
         ↓ parse_questions.py
      generated/questions.json   ← 程序只读，不提交 Git
         ↓ 查重 Agent
      duplicates/
         ↓
      rejected/   canonical/（远期）   bank/（500+ 题后）
```

| 目录 | 职责 |
| --- | --- |
| `question_sources/` | 来源索引 |
| `raw/` | 未整理堆积 |
| `categories/` | **编辑源** — 问题地图（允许重复、变体） |
| `schema/` | 格式规范 v0.2 + JSON Schema |
| `scripts/` | `parse_questions.py` |
| `generated/` | 编译产物（gitignore `*.json`） |
| `duplicates/` | 查重报告 |
| `rejected/` | **文件级**淘汰（不进 JSON 的来源） |
| `canonical/` | 远期标准题（目录表达，不用 status:canonical） |
| `prompts/` | 整理 / 查重 Agent |
| `bank/` | 500+ 题后再建设 |

---

## 两层生命周期

| | 目录（文件） | metadata（题目） |
| --- | --- | --- |
| 管什么 | raw 在哪、是否已整理、来源是否淘汰 | 题是否 active / deprecated |
| 例子 | `rejected/问题库-004-review.md` | `status: deprecated` |

**categories** = 人类按「问什么」浏览；**tags / type / interaction** = 程序检索。

---

## 分类体系

| 文件 | category slug |
| --- | --- |
| [现实问题.md](./categories/现实问题.md) | `real` |
| [情感问题.md](./categories/情感问题.md) | `emo` |
| [决策问题.md](./categories/决策问题.md) | `dec` |
| [状态问题.md](./categories/状态问题.md) | `sta` |
| [自我认知.md](./categories/自我认知.md) | `self` |
| [价值问题.md](./categories/价值问题.md) | `val` |
| [其他.md](./categories/其他.md) | `oth` |

见 [prompts/分类原则.md](./prompts/分类原则.md)。

---

## Agent 与脚本

| 步骤 | 工具 |
| --- | --- |
| 整理 | [问题整理提示词.md](./prompts/问题整理提示词.md) |
| 编译 | `python questions/scripts/parse_questions.py` |
| 查重 | [问题查重提示词.md](./prompts/问题查重提示词.md) |

整理 Agent：**不分析、不 mapsTo、不读 02**。

---

## 第二阶段（暂不做）

500+ 题后：`bank/`、`mapsTo`、引擎 JSON 导出。见 [design/engine.md](../design/engine.md)。
