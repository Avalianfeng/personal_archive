# rejected · 题库墓地

淘汰但**值得留底**的题目与踩坑记录。预期：收集大量题 → 精选少量 → 大量淘汰。

淘汰题不是垃圾。记录「什么问题不值得问」与未来价值可能不低于 `bank/`。

**文件生命周期** — 与题目 `status` 无关。见 [schema/格式规范.md §两层生命周期](../schema/格式规范.md)。

残缺 raw **从未成为 Question**，故不用 `status: rejected`；用本目录 `{文件名}-review.md` 记录。

## 用法

### 从 categories / bank 淘汰单题

1. 从 `categories/` 或 `bank/` **复制**（非剪切）到本目录
2. 保留完整 Markdown 或 JSON，并记录淘汰原因
3. 在 [_index.md](./_index.md) 追加索引行

### raw 级 review（损坏 / 残缺 / 错误复制）

当 raw 材料无法整理、不应强行入库时：

1. 新建 `{原文件名}-review.md`（如 `问题库-004-review.md`）
2. 说明：来源、问题、建议处置（放弃 / 重新采集 / 部分可用）
3. 在 `_index.md` 追加索引行
4. **不删除** raw 原文件（留作采集记录）

**示例**：`问题库-004` — PANAS 与 SWLS 混杂残缺版 → `rejected/问题库-004-review.md`

## 按原因归档（Markdown）

除单题文件外，可按原因维护汇总文件：

| 文件（示例） | 说明 |
| --- | --- |
| `引导性问题.md` | 引导性过强，易诱发表演或社会期望 |
| `信息密度低.md` | 答后几乎无有效信息 |
| `重复问题.md` | 与已有题完全重复（查重后确认） |

## 淘汰原因枚举

| reason | 说明 |
| --- | --- |
| `duplicate` | 与 categories/bank 中已有题**完全重复** |
| `leading` | 引导性过强 |
| `low_density` | 信息密度低 |
| `wrong_category` | 分类错误（可改写后回到 categories） |
| `scope_mismatch` | 与建档目标不符 |
| `superseded` | 被更好的改写版替代 |
| `corrupted` | 内容损坏，无法恢复 |
| `incomplete` | 残缺采集（量表不全、选项缺失） |
| `copy_error` | 错误复制（多量表混杂、网页残留） |

## JSON 淘汰（第二阶段）

工程化后的 JSON 题可追加：

```json
"rejected": {
  "date": "2026-06-14",
  "reason": "duplicate",
  "note": "与 Q-EMO-001 语义重复",
  "superseded_by": "Q-EMO-002"
}
```

或同名旁加 `{id}_rejected.md` 说明文件。

## 模板

单题淘汰见 [_template.md](./_template.md)。raw review 可复用其「元信息 + 说明」结构，原题摘要改为 raw 片段描述。
