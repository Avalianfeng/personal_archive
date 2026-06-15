# draft · 草稿题库

已结构化、待对齐 `mapsTo` 或 `dimensions` 的题目。

## 用法

1. 从 `inbox/` 或 `research/sources/` 改写后,复制 [_question.example.json](./_question.example.json) 为新文件
2. 命名建议:`INF_REL_001.json`(推断层)或 `ARC_BIO_001.json`(档案层)
3. 审阅通过后迁入 `bank/archive/` 或 `bank/inference/`
4. 不通过则**复制**到 `rejected/`,保留原 draft 或删除(建议保留至 rejected 确认后)

## 硬性规则

- 禁止 `analysis_hint`、禁止选项直接映射人格类型
- 推断层:只有 `evidence_tags`(行为/倾向证据词)
- 档案层(`layer: archive`):可省略 `evidence_tags`,强调事实字段
- `source_type` 必填;`information_density` 现阶段填 `null`
