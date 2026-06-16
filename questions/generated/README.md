# generated · 编译产物

**禁止手改。** 由 [`scripts/parse_questions.py`](../scripts/parse_questions.py) 从 `categories/*.md` 自动生成。

## 生成

```bash
python questions/scripts/parse_questions.py
```

输出：`questions.json`（本地使用，**不提交 Git**）。

## 用途（未来）

- 问题引擎读取
- 跨字段搜索（type、interaction、tags、subcategory、status）
- 维度映射阶段的输入（非整理阶段）

## 规则

- 克隆仓库后需自行运行脚本生成本地 JSON
- categories 变更后应重新 generate 并验证
