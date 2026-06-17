# source_library/ · Level 1 来源文献馆

研究材料、访谈协议、方法论来源。**不是题库**，永不 bulk 导入 `question_registry`。

## 放哪、链哪

| 内容 | 物理位置 | 卡片怎么写 |
| --- | --- | --- |
| **来源卡片**（元数据 + 整理说明） | `source_library/*.md` | 本目录，一条来源一张卡 |
| **待整理全文**（md / PDF） | `attachments/pending/` | `[附件](attachments/pending/文件名)` |
| **已整理原材料**（整理时对照的全文） | `attachments/processed/` | `[附件](attachments/processed/文件名)` |
| **测评脚本**（.js / .ts，只作参考） | `imports/external/` | `[脚本](../../imports/external/文件名)` |

卡片在 `source_library/`，附件在 `attachments/`，代码在 `imports/external/`。**不要**再使用已删除的 `raw/` 路径。

附件与外部脚本默认 **gitignore**（本地保留）；目录内 README 可入 Git 说明结构。

## SOURCE_CARD

每个卡片 md 建议头部：

```markdown
<!-- SOURCE_CARD
type: interview_protocol | question_list | scale | code_reference
status: organized | pending
priority: P1
ingest: never_bulk
attachments: attachments/pending/foo.pdf
-->
```

## 工作流

1. 在 `source_library/` 维护来源卡片（类型、优先级、整理注意）
2. 全文放进 `attachments/pending/` 或 `processed/`，卡片内链到相对路径
3. 测评脚本放进 `imports/external/`，卡片链到 `../../imports/external/…`
4. Agent 从来源**提炼**题目 → `imports/pending/*.jsonl` → `ingest.py`

## 子目录

| 路径 | 内容 |
| --- | --- |
| `attachments/pending/` | 待整理 md / PDF |
| `attachments/processed/` | 已整理过、仍要保留对照的全文 |
| `../imports/external/` | 仅作参考的测评脚本（禁止 bulk 入库） |

## Git 恢复说明（2026-06）

`raw/` 在 V2 迁移时误删；已从 commit `87077c7` 恢复到上述路径。**无法从 Git 恢复**的项（从未提交）：带 `[批次]` / `[P1]` 等前缀的旧文件名——恢复后使用 Git 中的原始文件名，卡片已对齐。
