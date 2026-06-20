# PVQ · 肖像价值观问卷

| 字段 | 值 |
| --- | --- |
| 类型 | 量表 |
| 语言 | en → zh（整理时译） |
| raw 路径 | [attachments/pending/问题库-003.md](attachments/pending/%E9%97%AE%E9%A2%98%E5%BA%93-003.md) |
| 整理优先级 | **P2** |
| 状态 | **已整理（实验 · 2026-06-17）** |

## 简介

Portrait Values Questionnaire（PVQ），约 40 题。「She…」第三人称描述 + 6 级「像我」量表。来源：https://aidaform.com/templates/pvq-test.html

## 整理注意

- 第三人称改第二人称或保留「某人」比较句式
- 题型：`agreement`；`interaction: rating`
- 主要归入：**价值问题**（`category: val`）
- 选项锚点：not like me at all … very much like me（入库为 6 级 `{key,text}` options）

## 整理记录（2026-06-17 实验）

| 项 | 值 |
| --- | --- |
| jsonl | `05-导入队列-Imports/01-pending-待入库/PVQ-20260617.jsonl` → `05-导入队列-Imports/02-processed-已入库/PVQ-20260617_ingested_20260617T044358Z.jsonl` |
| 入库题数 | **40**（Q-VAL-037 … Q-VAL-076） |
| 子分类 | **个人价值观**（新增，由 sync 写入 `02-问题地图-Views/价值问题.md`） |
| system_unaskable | 0（全部通过） |
| ingest | 成功；首跑 sync 因 options 格式与 schema 不一致失败，修正后 `manage sync` 通过 |
| duplicate_scan | 0 组完全重复 |
| doctor | OK |

## 备注

raw 文件无标准批次头；整理时 `source: PVQ`。options 须用 `[{"key":"1","text":"…"},…]`，非字符串数组（见 `schema/question.schema.json`）。
