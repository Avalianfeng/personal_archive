# personal_archive · 个人分析体系(文字仓库)

> 用「人物档案」作载体,表达并验证**我自己对人的分析体系与世界观**。
> 本仓库只放文字(立意、目录、金样、设计笔记);代码已整体移至 `D:\personal_archive_code`,引擎阶段再启用。
> **项目共识快照** → [项目状态.md](项目状态.md)

---

## 当前位置

```text
L0 输入 intake-v1          ✅ 冻结
L1 分析 report-v1           ✅ 第二稿(中间层)
产物 A analysis-report-v1   ⏳ python samples/generate_products.py a
产物 B person-archive-v1    ⏳ python samples/generate_products.py b(核心档案含§2人生经历)
多模型 L1 对比              🔧 python experiments/run_model_compare.py
questions/ 问题库            🔧 raw 堆题 → categories 整理
动态发掘 / 分题 prompts     ❌ 产物定稿后
引擎 / Web                  ❌ personal_archive_code
```

---

## 快速命令

```bash
# .env: DEEPSEEK_API_KEY=sk-...

# L1 → 产物 A(分析报告) + 产物 B(人物档案)
python samples/generate_products.py both

# 同 intake、同 prompt,换模型看 L1 差异
python experiments/run_model_compare.py --models deepseek-v4-flash,deepseek-v4-pro
```

---

## 文档地图

| 文件 | 是什么 |
| --- | --- |
| [项目状态.md](项目状态.md) | **项目演变 + 阶段 + 索引**(换模型/隔久必读) |
| [01-立意与分析体系.md](01-立意与分析体系.md) | 立意、原则、路线 |
| [02-档案目录.md](02-档案目录.md) | 认识论目录 §0–§13 |
| [questions/README.md](questions/README.md) | **问题库**:raw → categories → bank 精选 |
| [questions/prompts/问题整理提示词.md](questions/prompts/问题整理提示词.md) | 整理 Agent 提示词(核心) |
| [questions/bank/inference/dimensions.md](questions/bank/inference/dimensions.md) | 推断层维度树(含 current_state) |
| [samples/intake-v1.md](samples/intake-v1.md) | L0 输入金样(冻结) |
| [samples/report-v1.md](samples/report-v1.md) | **L1 分析中间层** |
| [design/分析报告目录.md](design/分析报告目录.md) | 产物 A 结构(含可选【深度观察】) |
| [design/核心档案目录.md](design/核心档案目录.md) | 产物 B · 核心档案(§2 人生经历为主体) |
| [design/时期快照目录.md](design/时期快照目录.md) | 产物 B · 时期快照(动态层) |
| [design/人物档案目录.md](design/人物档案目录.md) | 产物 B 索引(指向上述两文件) |
| [samples/generate_products.py](samples/generate_products.py) | L1 → A/B 生成 |
| [experiments/](experiments/) | 多模型对比实验 |
| [design/intake-notes.md](design/intake-notes.md) | 提问工程(`{}` 要点) |
| [design/engine.md](design/engine.md) | 引擎架构(后期) |

---

## 三层 + 双产物

```text
初级层(现在)   raw/ → categories/     问题地图
精选层(未来)   categories/ → bank/    JSON 工程化(phase-2)
档案层(事实)   bank/archive/          → 产物 B 核心档案
推断层(证据)   bank/inference/        → L1 report-v1 → 产物 A + B
```

流水线:

```text
intake (L0) → report-v1 (L1 分析) → 产物 A 解释报告 / 产物 B 人物档案
```

L1 不是给用户看的终稿;产物 A/B 目录在 `design/`,脚本在 `samples/generate_products.py`。

---

## 代码仓库

`D:\personal_archive_code` — 人格深潜、引擎骨架。设计以 `design/engine.md` 为准。
