# raw · 原始问题堆积

**文件夹 = 处理阶段**；**文件名前缀 = 优先级与类型**。与 [question_sources/](../question_sources/README.md) 卡片前缀联动。

```text
raw/
├── pending/      待整理队列（新 material 默认位置）
└── processed/    已整理完成（移入，不删除）
```

## 一眼看懂：pending 文件名前缀

| 前缀 | 含义 | 示例 |
| --- | --- | --- |
| `[P1]` | 整理优先级 P1 | `[P1] The Life Story Interview.md` |
| `[P2]` | 整理优先级 P2 | `[P2] 自尊量表.md` |
| `[P3]` | 整理优先级 P3 | `[P3] MBTI.js` |
| `[批次]` | 手工批次 dump，来源未单独建卡 | `[批次] 问题库-001.md` |
| `[元]` | 非题干（链接池等），**不送整理 Agent** | `[元] other_info.md` |

`processed/` 内文件**不加前缀**——目录本身表示「已处理」。

## 工作流

```text
采集 → raw/pending/[Px] 原文件名
         ↓ 在 question_sources 建/改 [待整理][Px] 卡片
整理 Agent → categories/
         ↓ build_questions.py
残缺 → rejected/
         ↓
移至 raw/processed/原文件名
         ↓
卡片前缀改为 [已整理][Px]
```

### 流转检查清单

| 步骤 | raw | question_sources 卡片 |
| --- | --- | --- |
| 新采集入队 | 放入 `pending/`，加 `[Px]` 或 `[批次]` | `[待整理][Px]` 或 `[待采集]` |
| 整理完成 | `pending/` → `processed/` | `[待整理]` → `[已整理]` |
| 拒绝整理 | 可留 `processed/` 或删 | → `[已拒绝]` |
| 改优先级 | 改 `pending/` 文件名前缀 | 同步改卡片 `[Px]` |

新批次命名：`[批次] 问题库-NNN.md` 放入 `pending/`；确认来源后改为 `[Px]` 并建卡片。

## 职责分工

| 目录 | 回答什么 |
| --- | --- |
| [question_sources/](../question_sources/) | 来源从哪来、整理状态（卡片改前缀，不移动） |
| `raw/pending/` | 哪些 raw 还没处理？按 `[P1]`→`[P3]` 排序即工作队列 |
| `raw/processed/` | 哪些已进 categories？ |
| [categories/](../categories/) | 整理后的问题地图 |

规范：[整理规范-v0.1.md](../整理规范-v0.1.md) · [schema/格式规范.md](../schema/格式规范.md)
