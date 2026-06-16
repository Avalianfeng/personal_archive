# bank · 精选题库

从 [categories/](../categories/README.md) 人工或 Agent 筛选后的**高质量子集**。

## 现阶段：不建设

**覆盖度不足**。迁入 `bank/` 的前提：**500+ 高质量整理题**完成。见 [整理规范-v0.1.md §十一](../整理规范-v0.1.md)。

现阶段本目录保持为空（仅 README 与第二阶段预留子目录）。

## 与 categories 的关系

```text
categories/   全量分类地图（含重复、变体、待改写题）
     ↓ 500+ 题后精选
bank/         审过的高质量题
```

## 子目录（第二阶段预留）

| 目录 | 用途 | 阶段 |
| --- | --- | --- |
| `archive/` | 档案层定稿（事实类 JSON） | phase-2 |
| `inference/` | 推断层定稿（证据 → AI） | phase-2 |

现阶段 `archive/`、`inference/` 仅保留 README 与 [dimensions.md](./inference/dimensions.md)，不填充 JSON 定稿题。

## 迁入条件（未来）

从 `categories/` 精选：信息密度高、无强引导性、表述清晰、与已有题非完全重复。审阅通过后可工程化为 JSON 迁入 `bank/archive/` 或 `bank/inference/`。

旧版 JSON 格式与迁入规则见 [archive/questions-v1/draft/](../../archive/questions-v1/draft/)。
