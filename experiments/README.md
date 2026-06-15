# 同内容 · 多模型对比实验

> **目的**：固定同一份输入语料 + 同一套 L1 分析提示词（归档），换不同 AI 模型，看结论是否差异巨大。
> **注意**：L1 管线已废止为活跃流水线；本实验仅作历史方法验证。

---

## 输入（固定）

| 项 | 文件 |
| --- | --- |
| 语料 | [samples/intake-v1-clean.md](../samples/intake-v1-clean.md) |
| 提示词 | [archive/reference/l1-analysis-v1.md](../archive/reference/l1-analysis-v1.md) |
| 目录摘要 | [02-维度地图-dimensions.md](../02-维度地图-dimensions.md)（脚本自动截断） |

---

## 运行

```bash
# .env 中配置 DEEPSEEK_API_KEY=sk-...

python experiments/run_model_compare.py

python experiments/run_model_compare.py --models deepseek-v4-flash,deepseek-v4-pro

python experiments/run_model_compare.py --models deepseek-v4-flash --dry-run
```

**产出**：`experiments/outputs/l1-{model}-{date}.md`

---

## 怎么读结果

1. 打开同一天的多个 `l1-*.md`
2. 对照综合观察与主题线 — 主干是否一致？
3. 结论用于评估**模型差异**，不再接入产物 A/B 生成（已废止）

---

## 文件

| 文件 | 作用 |
| --- | --- |
| [llm_client.py](./llm_client.py) | DeepSeek / OpenAI 兼容调用 |
| [run_model_compare.py](./run_model_compare.py) | 批量跑模型 |
| [outputs/](./outputs/) | 产出目录 |
