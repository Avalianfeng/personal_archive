# questions/ · 题库工程

> **功能**:题目从哪来、怎么管、怎么分层——与根目录 `archive/`(历史留底) 区分,专管**活跃中的题库**。
> **阶段**:骨架已建,内容手动填充;不做 CLI/Web,不自动生成 intake。
> **关联**:[02-档案目录.md](../02-档案目录.md) · [design/intake-notes.md](../design/intake-notes.md) · [archive/gpt-new-suggestion.md](../archive/gpt-new-suggestion.md)

---

## 三层模型

| 层 | 目录 | 回答什么 |
| --- | --- | --- |
| **档案层** | `bank/archive/` | 这个人**是谁**(事实,不必 AI 推断) |
| **推断层** | `bank/inference/` | 这个人**可能怎样**(证据 → AI 推断) |
| **报告层** | `design/` 产物 A/B | 如何组织成可读内容(不在本目录) |

推断层原则:**Question ≠ Analysis**。题目只产 `evidence_tags`,禁止 `analysis_hint` 或选项直接映射人格类型。

---

## 工作流

```text
外部来源 / 灵感          → research/sources/
零散批注 / 情境题        → inbox/
         ↓ 分类 + 改写
                      draft/  (JSON 结构化)
         ↓ 审阅
              bank/archive/ 或 bank/inference/
         ↓ 淘汰但留底
                      rejected/
```

| 阶段 | 目录 | 出去的条件 |
| --- | --- | --- |
| 收集 | `research/sources/` | 不要求 mapsTo |
| 待处理 | `inbox/` | 在 `_index.md` 标状态 |
| 草稿 | `draft/` | 有 id、type、mapsTo 或 dimension |
| 定稿 | `bank/` | 审过的正式题 |
| 淘汰 | `rejected/` | 记录原因,**不直接删除** |

---

## 文件格式

- **来源收集**:Markdown,见 [research/sources/_template.md](./research/sources/_template.md)
- **定稿题目**:JSON,见 [draft/_question.example.json](./draft/_question.example.json)
- **维度树**:见 [bank/inference/dimensions.md](./bank/inference/dimensions.md)

### JSON 硬性规则

1. 每题须 `mapsTo` 到 [02-档案目录.md](../02-档案目录.md) 三级条,或 `dimensions` 对齐 dimensions.md
2. `source_type` 必填(draft 起):`scale` | `interview` | `self_observation` | `intake_annotation` | `other`
3. `information_density` 现阶段填 `null`,日后标 low/medium/high 或 1–5
4. 档案层题可省略 `evidence_tags`;推断层题必须有

### 命名

- `inbox/`、`research/sources/`: `YYYY-MM-DD-短slug.md`
- 定稿 JSON: `{LAYER}_{维度}_{序号}.json`(如 `INF_REL_001.json`)

---

## 与现有文件

| 现有 | 关系 |
| --- | --- |
| `samples/intake-v1.md` `{}` 批注 | 金样冻结;批注逐条外迁到 inbox/research |
| `design/intake-notes.md` | 压缩索引;展开入口在本目录 |
| `design/engine.md` `questions.json` | 日后从 `bank/` 导出 |

---

## 下一阶段(本目录不做)

从海量题目中筛选**高信息密度**题(`information_density` 启用后)。`rejected/` 用于防重复踩坑与复盘。
