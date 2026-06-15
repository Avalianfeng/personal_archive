# bank/archive · 档案层定稿题库（phase-2）

> **现阶段**:空目录，仅作第二阶段预留。初级层题目在 [categories/](../categories/README.md)。

**层**:档案层 — 记录事实,不必 AI 推断。
## 内容

- 基本信息、经历、时间线、家庭、教育、职业等
- JSON 中 `"layer": "archive"`
- 可省略 `evidence_tags`,强调事实字段

## 迁入条件

从 `categories/` 精选并工程化为 JSON 后迁入:有 id、type、`mapsTo` 指向 [02-维度地图-dimensions.md](../../../02-维度地图-dimensions.md) 事实类三级条(如 §3 基础画像、§11 轨迹)。旧流程见 [archive/questions-v1/draft/](../../../archive/questions-v1/draft/)。
## 命名

`ARC_{主题}_{序号}.json`(如 `ARC_EDU_001.json`)
