# rejected · 题库墓地

淘汰但**值得留底**的题目与踩坑记录。预期：收集大量题 → 精选少量 → 大量淘汰。

淘汰题不是垃圾。记录「什么问题不值得问」与未来价值可能不低于 `bank/`。

## 用法

1. 从 `categories/` 或 `bank/` **复制**（非剪切）到本目录
2. 保留完整 Markdown 或 JSON，并记录淘汰原因
3. 在 [_index.md](./_index.md) 追加索引行

## 按原因归档（Markdown）

除单题文件外，可按原因维护汇总文件：

| 文件（示例） | 说明 |
| --- | --- |
| `引导性问题.md` | 引导性过强，易诱发表演或社会期望 |
| `信息密度低.md` | 答后几乎无有效信息 |
| `重复问题.md` | 与已有题语义重复 |

## 淘汰原因枚举

| reason | 说明 |
| --- | --- |
| `duplicate` | 与 categories/bank 中已有题语义重复 |
| `leading` | 引导性过强 |
| `low_density` | 信息密度低 |
| `wrong_category` | 分类错误（可改写后回到 categories） |
| `scope_mismatch` | 与建档目标不符 |
| `superseded` | 被更好的改写版替代 |

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
