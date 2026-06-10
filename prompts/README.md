# 分析提示词（Processor）

> **功能**：存放 `ai_extract` / `ai_synthesize` 等 Processor 引用的提示词模板。  
> **定位**：原话与结构化答案 → **档案语言** → 写入 PersonModel；报告只读 Model。  
> **状态**：占位；待 `person-analyze-report-v1` 定稿后反推  
> **关联**：[person-archive-engine.md](../docs/person-archive-engine.md) · [archive-catalog-v1.md](../archive-catalog-v1.md) · [plugins/core-intake/processors.yaml](../plugins/core-intake/processors.yaml)

---

## 分层

| 目录 | Processor | 输入 → 输出 |
| --- | --- | --- |
| [extract/](./extract/) | `ai_extract` | 单题/单条回答 → 对应三级条的档案语言段落 |
| [synthesize/](./synthesize/) | `ai_synthesize` | 多源/跨章 → §1.1 核心印象、§13 综合观察等 |

## 命名约定（草案）

```text
extract/{catalog-id}.md      # 例：extract/2-3-2-tension.md
synthesize/section-{n}.md    # 例：synthesize/section-13.md
```

每份提示词头部注明：`mapsTo` 三级条 ID、输入字段、语气约束（Frame）、禁止事项（如 MBTI 口吻入主文）。

## 金样驱动

**裁判文档**：定稿后的 [person-analyze-report-v1.md](../docs/persona-samples/person-analyze-report-v1.md)。  
写法：对比「手填输入」与「报告输出」，逐条写 extract/synthesize 提示词，直到引擎输出接近金样。
