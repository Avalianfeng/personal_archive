# raw · 原始问题堆积

```text
raw/pending/     待整理队列（新 material 默认放这里）
raw/processed/   已整理完成（移入，不删除）
```

## 工作流

```text
raw/pending/X
  → 整理 Agent → categories/
  → build_questions.py
  → rejected/（残缺 / system_unaskable）
  → 移至 raw/processed/X
  → 更新 question_sources 卡片状态
```

## 职责分工

| 目录 | 回答什么 |
| --- | --- |
| [question_sources/](../question_sources/) | 来源从哪来（档案馆，卡片不移动） |
| `raw/pending/` | 哪些还没处理？ |
| `raw/processed/` | 哪些已进 categories？ |
| [categories/](../categories/) | 整理后的问题地图 |

新批次命名：`问题库-NNN.md` 放入 `pending/`。

规范：[整理规范-v0.1.md](../整理规范-v0.1.md) · [schema/格式规范.md](../schema/格式规范.md)
