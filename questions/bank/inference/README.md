# bank/inference · 推断层定稿题库（phase-2）

> **现阶段**:仅保留 [dimensions.md](./dimensions.md) 作只读参考。初级层题目在 [categories/](../../categories/README.md)。

**层**:推断层 — 行为/情境题 → `evidence_tags` → AI 推断。
## 内容

- 情境题、行为选择题、短开放补充
- JSON 中 `"layer": "inference"`
- 必须有 `evidence_tags`;禁止 `analysis_hint`

## 迁入条件

从 `categories/` 精选并工程化为 JSON 后迁入:有 id、type、`mapsTo` 或 `dimensions` 对齐 [dimensions.md](./dimensions.md)。旧流程见 [archive/questions-v1/draft/](../../../archive/questions-v1/draft/)。
## 命名

`INF_{维度缩写}_{序号}.json`(如 `INF_REL_001.json`)

## 维度树

见 [dimensions.md](./dimensions.md) — 写题之前先定结构,不要从 200 题开始。
