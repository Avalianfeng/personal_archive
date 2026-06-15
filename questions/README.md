# questions/ · 人物建档问题库

> questions/ 是人物建档**问题库**。当前阶段目标不是推断人格，而是持续**收集、整理和筛选**高质量问题，形成可浏览、可扩展的**问题地图**。
>
> **关联**：[design/intake-notes.md](../design/intake-notes.md) · [02-维度地图-dimensions.md](../02-维度地图-dimensions.md) · [design/00-档案文件群-index.md](../design/00-档案文件群-index.md)

---

## 当前阶段（初级层）

```text
量表 / 访谈 / 灵感 / intake 批注
         ↓ 复制粘贴
      raw/问题库-NNN.md
         ↓ Agent + 问题整理提示词
      categories/*.md
         ↓ 人工精选（未来）
      bank/
         ↓ 淘汰留底
      rejected/
```

| 目录 | 职责 |
| --- | --- |
| `raw/` | 来源混杂的原始堆积，不要求分类 |
| `categories/` | 去重、归类、规范化后的分类地图 |
| `prompts/` | **核心** — 整理 Agent 提示词与分类原则 |
| `bank/` | 精选题库（现阶段可为空） |
| `rejected/` | 淘汰留底与踩坑记录 |

**本阶段不做**：`mapsTo` JSON 定稿、自动写入档案文件。

---

## 分类体系

| 文件 | 回答什么 | 对应档案文件 |
| --- | --- | --- |
| [现实问题.md](./categories/现实问题.md) | 发生过什么、是什么 | 05、06 |
| [情感问题.md](./categories/情感问题.md) | 感受什么、关系体验 | 04 |
| [决策问题.md](./categories/决策问题.md) | 怎么选择、怎么判断 | 03 |
| [状态问题.md](./categories/状态问题.md) | 现在怎么样 | 07 |
| [自我认知.md](./categories/自我认知.md) | 怎么看自己 | 01 |
| [价值问题.md](./categories/价值问题.md) | 认为什么重要 | 02 |
| [其他.md](./categories/其他.md) | 暂无法归入以上类 | — |

诚实度**不是独立分类** — 校验题加 `[校验]` 标签，归入内容所属类。

分类定义见 [prompts/分类原则.md](./prompts/分类原则.md)。

---

## 整理 Agent

将 [prompts/问题整理提示词.md](./prompts/问题整理提示词.md) 中「提示词正文」整段复制到对话，粘贴 `raw/` 内容即可。

Agent 只做：去重 → 归类 → 规范化 → 按格式输出 Markdown。**不分析、不推断。**

---

## 第二阶段（暂不做）

题库积累到 300+ 题后，再启用 JSON 工程化、`mapsTo`（对齐 [02 §14](../02-维度地图-dimensions.md)）、`information_density`。

预留资源：

- [bank/inference/dimensions.md](./bank/inference/dimensions.md) — 推断层维度树
- [archive/questions-v1/](../archive/questions-v1/) — 旧版骨架

---

## 与现有文件

| 现有 | 关系 |
| --- | --- |
| `samples/intake-v1.md` `{}` 批注 | 金样冻结；批注可摘录到 `raw/` |
| `samples/persona-v1/` | 金样档案文件群；问题整理目标侧面见上表 |
| `design/intake-notes.md` | 题面设计压缩索引 |
| `design/engine.md` | 日后从 `bank/` 导出 `questions.json` |
