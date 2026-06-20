# Adult Attachment Interview (AAI)

| 字段 | 值 |
| --- | --- |
| 类型 | 关系访谈（研究协议） |
| 语言 | en |
| raw 路径 | [attachments/pending/ADULT ATTACHMENT INTERVIEW PROTOCOL.md](attachments/pending/ADULT%20ATTACHMENT%20INTERVIEW%20PROTOCOL.md) |
| 整理优先级 | **P1** |
| 状态 | **已整理（2026-06-20）** |

## 简介

Mary Main 成人依恋访谈协议。聚焦童年与父母的依恋关系、丧失、虐待等。含大量**访谈者操作说明**与探针（probes）。

## 整理记录

| 项 | 值 |
| --- | --- |
| 入库题数 | **45**（Q-EMO-072 … Q-VAL-165 等，见 batch_delta_compact.md） |
| 子分类 | 亲密关系 · 哀伤与失去 · 家庭与成长 等 |
| jsonl | `05-导入队列-Imports/02-processed-已入库/AAI-20260620_ingested_20260620T153317Z.jsonl` |
| 批次 | Wave 2 · 与 Southern Oral 并行整理 → 单点 accept |
| rejected | 0 |

## 整理注意

- **只提取**可面向被访者的主问题；访谈者说明、评分提示、探针逻辑不入 categories
- 敏感主题（丧失、虐待）保留题干，但不做人格/依恋类型推断标注
- 典型 `回答形式: story`
- 主要归入：情感问题、现实问题（童年经历）
- **禁止** mapsTo 到依恋类型或诊断

## 版权

研究协议；勿商业再传播。标注 `来源: AAI Protocol (Main)`。
