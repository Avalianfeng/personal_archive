# 整理 Agent · 启动清单

> **复制本页 + [02-问题整理提示词.md](./02-问题整理提示词.md) 正文** 即可开始一批整理。  
> **禁止读**：`02-维度地图-dimensions.md` · `design/catalog/` · `samples/persona-v1/`

---

## 只读这 3 个文件（按顺序）

| # | 文件 | 用途 |
| --- | --- | --- |
| 1 | [00-整理规范-v1.0.md](../00-整理规范-v1.0.md) | jsonl 契约 · 量表 checklist · 批次验收 |
| 2 | [02-问题整理提示词.md](./02-问题整理提示词.md) | 去格式 · system_unaskable · 输出格式 |
| 3 | `01-文献与来源-Library/` 序号卡片 + 正文 md | 本批来源索引 + 原材料 |

**subcategory 犹豫时**追加：[03-分类原则.md](./03-分类原则.md)  
**options / 字段细节**：[02-schema-格式契约/01-格式规范.md](../02-schema-格式契约/01-格式规范.md)

---

## 产出

| 产物 | 路径 |
| --- | --- |
| 入库 jsonl | `questions/05-导入队列-Imports/01-pending-待入库/{source}-{YYYYMMDD}.jsonl` |
| rejected  sidecar（可选） | `questions/05-导入队列-Imports/01-pending-待入库/{source}-{YYYYMMDD}.rejected.jsonl` |

**options 必须是** `[{"key":"1","text":"…"},…]` 或 `options_ref`（见 [options_templates.yaml](../01-registries-规则真源/options_templates.yaml)），禁止字符串数组。

rejected sidecar 每行：`{"question":"…","reason":"intimate_dyadic","note":"…"}` — 不进 DB。

---

## 验收（收集期）

```bash
python questions/scripts/ingest.py --dry-run
python questions/scripts/manage.py accept --json
```

成功后必读：

- `questions/03-规则与审计-Meta/03-generated-审计产物/01-agent-Agent视图/batch_delta_compact.md` — 本批新题 compact（优先）
- `…/batch_delta.json` — 本批新 id
- `questions/03-规则与审计-Meta/03-generated-审计产物/health.json` — doctor 结果

**收集期不跑**查重/审查 Agent（见 [04-清理期Agent启动.md](./04-清理期Agent启动.md)）。

---

## 整理完成后

1. 回写 `01-文献与来源-Library` 卡片（见 [Library README](../../01-文献与来源-Library/README.md)）
2. 正文已整理的可保留原位或移 `_archive/`（可选）
3. 更新 [01-文献与来源-Library/README.md](../../01-文献与来源-Library/README.md) 索引表

---

## 量表 Portrait 改写（She → 你）

| 英文模式 | 中文输出 |
| --- | --- |
| Thinking up new ideas… is important to **her**. | **你**认为想出新点子、用原创方式做事很重要。 |
| **She** likes to do things in **her** own original way. | **你**喜欢按自己的方式做事。 |
| It is important to **her** to be rich. | 对你来说，变得富有很重要。 |
| **She** wants people to admire what **she** does. | 你希望在他人面前展示自己的能力。 |

整句合并为一条题干 + `type: agreement` + 6 级 options。

---

## tags 何时填写

| 情况 | 建议 |
| --- | --- |
| 题干明确涉及宗教信仰、仪式、神/灵性 | `tags: ["religion"]`（须已在 tags.yaml） |
| 题干涉及政治立场、选举、党派 | `tags: ["politics"]` 若已登记 |
| 普通价值观/人格陈述，无特定主题 | **省略 tags** |
| 不确定 tag 是否已登记 | **省略**；需要时走 registry 审核 |

宗教/政治**不新开一级分类**；按功能入 `val` / `real` 等，用 tags 检索。
