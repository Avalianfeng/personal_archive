# 同内容 · 多模型对比实验

> **目的**:固定同一份输入语料 + 同一套 L1 分析提示词,换不同 AI 模型,看**结论是否差异巨大**(模型智力/风格/稳定性),而非「纯答案 vs 含批注」。
> **旧 A/B 实验**(intake 贫语料 vs 富批注)已归档 → [archive/ab-intake-2026-06-13/](./archive/ab-intake-2026-06-13/)

---

## 输入(固定)

| 项 | 文件 |
| --- | --- |
| 语料 | [samples/intake-v1-clean.md](../samples/intake-v1-clean.md)(纯答案,无 `{}`/`<<>>`) |
| 提示词 | [prompts/l1-analysis-v1.md](../prompts/l1-analysis-v1.md) |
| 目录摘要 | [02-档案目录.md](../02-档案目录.md) 原则 + 章结构(脚本自动截断) |

---

## 运行

```bash
# .env 中配置 DEEPSEEK_API_KEY=sk-...
# 可选 OPENAI_API_KEY + --provider openai

# 默认跑两个 DeepSeek 模型
python experiments/run_model_compare.py

# 指定模型(逗号分隔)
python experiments/run_model_compare.py --models deepseek-chat,deepseek-reasoner

# 只写 prompt 不调 API
python experiments/run_model_compare.py --models deepseek-chat --dry-run
```

**产出**:`experiments/outputs/l1-{model}-{date}.md`

---

## 怎么读结果

1. 打开同一天的多个 `l1-*.md`
2. 对照 **§13 综合观察** 与 **主题线表** — 主干是否一致?
3. 若 3 个模型 80% 主题一致 → L1 结论对模型不敏感,可固定一个模型做产物 A/B
4. 若分歧大 → 记录在 `experiments/outputs/compare-{date}.md`(手填),或日后加自动 diff 脚本

**不要**用本实验验证「贫语料够不够」——那是已归档的 A/B 实验;本实验只验证**模型差异**。

---

## 文件

| 文件 | 作用 |
| --- | --- |
| [llm_client.py](./llm_client.py) | DeepSeek / OpenAI 兼容调用 |
| [run_model_compare.py](./run_model_compare.py) | 批量跑模型 |
| [outputs/](./outputs/) | 产出目录(gitignore 可选) |
