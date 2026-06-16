# generated · 编译产物

**禁止手改。** 由 [`scripts/build_questions.py`](../scripts/build_questions.py) 从 `categories/*.md` + `registries/*.yaml` 自动生成。

## 生成

```bash
python questions/scripts/build_questions.py
```

| 文件 | 内容 |
| --- | --- |
| `questions.json` | 题目（含 `prerequisites` 若已标注） |
| `stats.json` | 统计 + `unknown_prerequisites` / `unknown_tags` |
| `duplicate_hints.json` | 重复 text 提示 |
| `registries.json` | 标准库快照 |

本地使用，**不提交 Git**。

## 用途（未来）

- 问题引擎：prerequisites → 事实仓库 → 解锁
- 跨字段搜索（type、interaction、tags、prerequisites、subcategory、status）
- 维度映射阶段的输入（非整理阶段）

## 规则

- 克隆仓库后需自行运行脚本生成本地 JSON
- categories 或 registries 变更后应重新 generate 并验证
