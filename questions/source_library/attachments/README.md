# attachments/

来源全文的本地存放区（PDF、md 等）。**gitignore**，仅 README 入 Git。

| 子目录 | 用途 |
| --- | --- |
| `pending/` | 待整理原材料 |
| `processed/` | 已整理但仍需保留对照的全文 |

卡片引用示例（相对 `source_library/`）：

- `[待整理附件](attachments/pending/The Life Story Interview.md)`
- `[已整理附件](attachments/processed/good question.md)`

**禁止** ingest 或 PDF 解析 bulk 入库。
