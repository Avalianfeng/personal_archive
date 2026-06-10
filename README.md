# personal_archive · 个人分析体系(文字仓库)

> 用「人物档案」作载体,表达并验证**我自己对人的分析体系与世界观**。
> 本仓库只放文字(立意、目录、金样、设计笔记);代码已整体移至 `D:\personal_archive_code`,引擎阶段再启用。

---

## 当前位置(打开本仓库先看这里)

```text
① 输入金样(手填问卷)      ✅ 完成,已冻结
② 输出金样(分析报告)      ◀ 现在:第二稿(开放问题已答并并入正文),等你逐章定稿
③ 反推 prompts             未开始(以②定稿为裁判;须满足「贫语料假设」,见 01 §5.7)
④ 引擎闭环(代码迁回)      未开始
⑤ Web 采集                 后期
```

**下一步行动**:逐章审改 [samples/report-v1.md](samples/report-v1.md) 第二稿,定稿。改报告时做被分析者,改结构时回到立意文档(分轨约定见 01 §7)。

## 文档地图(全部文件)

| 文件 | 是什么 | 状态 |
| --- | --- | --- |
| [01-立意与分析体系.md](01-立意与分析体系.md) | 第一文档:立意、路线、原则、验收 | AI 初稿,待你定稿 |
| [02-档案目录.md](02-档案目录.md) | 「看懂一个人要看哪些维度」§0–§13 三级结构 | V1 稳定 |
| [samples/intake-v1.md](samples/intake-v1.md) | **输入金样**:手填问卷原版(答案+`{}`/`<<>>`批注) | 冻结,不改 |
| [samples/report-v1.md](samples/report-v1.md) | **输出金样**:人物分析报告 | AI 初稿,待你定稿 |
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
