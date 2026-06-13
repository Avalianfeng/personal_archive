# personal_archive · 个人分析体系(文字仓库)

> 用「人物档案」作载体,表达并验证**我自己对人的分析体系与世界观**。
> 本仓库只放文字(立意、目录、金样、设计笔记);代码已整体移至 `D:\personal_archive_code`,引擎阶段再启用。

---

## 当前位置(打开本仓库先看这里)

```text
① 输入金样(手填问卷)      ✅ 完成,已冻结
② 分析中间层(L1)          ◀ 现在:A/B 实验 + 审 report-v1(体系构建者视角)
③ 展示报告(L2)            未开始(从 L1 定稿后再写)
④ 反推 prompts             未开始(以 L1 定稿为裁判)
⑤ 引擎闭环                 未开始
⑥ Web 采集                 后期
```

**你具体该做什么(2026-06-11)**:

1. **不要**把 `report-v1.md` 当最终报告逐字润色——它是 L1 早期样,任务是**验读法**不是改文笔
2. **跑实验** A/B:见 [experiments/protocol-ab-intake.md](experiments/protocol-ab-intake.md)(纯答案 vs 含批注,DeepSeek 全卷一次分析)
3. **填对比表** [experiments/compare-template.md](experiments/compare-template.md):一致=问卷可推;分歧=元认知/追问
4. L1 定稿后,再写 L2 展示层

**分轨**:改 report / 跑实验 / 填对比 = 体系构建者;不要在同一次会话里混「我被分析到了」的自我沉浸。

## 文档地图(全部文件)

| 文件 | 是什么 | 状态 |
| --- | --- | --- |
| [01-立意与分析体系.md](01-立意与分析体系.md) | 第一文档:立意、路线、原则、验收 | AI 初稿,待你定稿 |
| [02-档案目录.md](02-档案目录.md) | 「看懂一个人要看哪些维度」§0–§13 三级结构 | V1 稳定 |
| [samples/intake-v1.md](samples/intake-v1.md) | **L0 输入金样**:手填问卷(答案+批注) | 冻结 |
| [samples/intake-v1-clean.md](samples/intake-v1-clean.md) | **L0 导出**:纯答案(实验 A 用) | 可重生成 |
| [samples/report-v1.md](samples/report-v1.md) | **L1 中间层**(早期样,含部分 L2 口吻) | 待实验对照后定稿 |
| [experiments/](experiments/) | A/B 协议、DeepSeek 脚本、对比表 | 进行中 |
| [prompts/full-report-v1.md](prompts/full-report-v1.md) | 全卷一次分析提示词 | V1 |
| [design/engine.md](design/engine.md) | 引擎架构(PersonModel / Processor / 插件) | 有效,引擎阶段用 |
| [design/meta-frame-moment.md](design/meta-frame-moment.md) | §0 Meta 语境层字段与向导文案 | 草案 |
| [design/skip-semantics.md](design/skip-semantics.md) | 跳过/拒答的存储与报告语义 | 草案 |
| [design/intake-notes.md](design/intake-notes.md) | 题面设计要点压缩版(原 13 分册占位) | 题库阶段用 |
| [archive/](archive/) | 归档:gpt 评审、旧项目指南、报告写法决策记录 | 只读留底 |

## 工作方式

- **金样驱动**:每一步的产出裁判下一步,不跳步。理由与完整路线见 [01-立意与分析体系.md](01-立意与分析体系.md) §4。
- **AI 起草 → 你定稿**:重要文本(立意、报告)由 AI 出初稿并标注〔推断〕/〔待你确认〕,你修改后成为定稿。
- **冻结纪律**:`samples/intake-v1.md` 永不修改;立意定稿后,旧文档与本文冲突处以新文档为准。

## 代码仓库

`D:\personal_archive_code` — 人格深潜 App(可运行)、引擎/插件骨架。使用前 `pnpm install`。
设计文档以本仓库 `design/engine.md` 为准;何时迁回见路线 ④。
