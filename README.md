# personal_archive · 个人分析体系（文字仓库）

> 用「人物档案」作载体，建立并验证**一套关于如何认识人、发掘人、记录人的文本工程**。
> 本仓库只存放文字：立意、设计契约、金样档案、问题库、实验记录。**不含可执行产品代码**。
>
> **最后更新**：2026-06-16

---

## 1. 这个项目是什么

### 1.1 立意

「人物档案」是**载体和验证场**，不是最终目的。真正在构建的是：**我自己的分析体系与世界观**——用对人的思考与认识，搭一套可复用的认识模型。

护城河不在报告文笔或某个 Prompt，而在**提问、追问、对话式发掘的设计**。

### 1.2 当前核心产出

| 产出 | 位置 | 说明 |
| --- | --- | --- |
| **人物档案文件群** | `samples/persona-v1/`（**本地金样**） | 8 个 Markdown 文件，按「构成侧面」拆分；每文件 §1 记录 + §2 解读 + §3 开放问题 |
| **L0 输入金样** | `samples/intake-v1.md`（**本地**） | 手填原始语料，**已冻结**，不再修改 |
| **问题地图** | `questions/categories/` | 结构化题库，与档案侧面、维度地图对齐 |
| **设计契约** | `01` · `02` · `design/` | 宪法、认识论本体、阅读顺序、各侧面目录模板 |

### 1.3 当前不在做什么

- 不运行「intake → L1 报告 → 单文件产物」旧流水线（历史见 `archive/reference/`）
- 不做 `question_guides/`（怎么问）、`analysis_guides/`（按题预置解读）
- 不做多用户实验、动态追问规范、档案自动生成脚本（均未开始）
- 引擎闭环与 Web 采集属于远期路线，文字侧定稿后再考虑

---

## 2. 设计原则

完整条文见 [01-立意与分析体系.md](01-立意与分析体系.md) §2。以下为入口级摘要。

### 2.1 档案与内容

1. **档案是关于人的，不是关于问题的** — 每一节回答「了解这个人」，而非「第几题放了什么」。
2. **建档优先于测评** — 正文不以类型学标签为主体；量表结论最多作附录参考。
3. **手填金样冻结** — `intake-v1.md` 的答案与 `{}` / `<<>>` 批注不再改动。
4. **贫语料假设** — 默认输入是「选项 + 简短回答」；深度靠追问设计与萃取，不靠用户写长文。
5. **防语料污染** — 第一版生长在单一 Persona 上；分析模式在第二个 Persona 与外部校准前只享候选地位。
6. **分析者在场** — 解读带署名性，是「某个分析体系对一个人的解读」，落在各文件 §2，而非独立分析报告。

### 2.2 文件群结构（当前架构）

7. **按构成侧面组织** — 不按目的（记录 vs 分析）拆文件；阅读时一次只打开一个侧面。
8. **分析溶解于档案** — 每文件强制三层：§1 原始记录 / §2 当前解读 / §3 开放问题；禁止混写。
9. **档案文件群是活的** — 结构稳定，内容可长期更新、重新解读、标注确信度。

### 2.3 工程与顺序

10. **设计顺序不可颠倒** — 输入金样 → 档案文件群 → 问题地图 → 引擎 → Web；上一步产出能裁判下一步质量。
11. **不要让用户主导结构** — 体系引导与发掘；用户选模式定方向，不由用户即兴定义目录。
12. **显式分轨** — 改 `persona-v1/` 时做被分析者；改 `01` / `design/` / 项目状态时做体系构建者；不在同一次工作中混用。

### 2.4 三个层次不要混

| 层次 | 文件 | 回答的问题 |
| --- | --- | --- |
| **认识论** | [02-维度地图-dimensions.md](02-维度地图-dimensions.md) | 看一个人要看哪些维度（§0–§14）；引擎与题库 `mapsTo` 的坐标 |
| **阅读契约** | [design/00-档案文件群-index.md](design/00-档案文件群-index.md) | 档案文件群怎么读、更新频率、与题库的对应 |
| **侧面目录** | [design/catalog/](design/catalog/) | 每个文件内 §1/§2/§3 下有哪些节标题 |
| **金样内容** | [samples/persona-v1/](samples/persona-v1/)（**仅本地，见 [samples/README.md](samples/README.md)**） | 具体某个人的记录与解读 |

**02 是维度坐标，不是阅读顺序。** 阅读顺序只看 `design/00-档案文件群-index.md`。

---

## 3. 项目状态（2026-06-16）

### 3.1 已完成

| 模块 | 状态 | 说明 |
| --- | --- | --- |
| 宪法与同步 | ✅ | [01-立意与分析体系.md](01-立意与分析体系.md)、[SYNC-CHECKLIST.md](SYNC-CHECKLIST.md) |
| 维度地图 | ✅ | [02-维度地图-dimensions.md](02-维度地图-dimensions.md) §0–§14，含文件群映射 |
| 档案设计契约 | ✅ | `design/00-index` + `design/catalog/` 各侧面模板 |
| L0 输入 | ✅ 冻结 | `samples/intake-v1.md`、`intake-v1-clean.md` |
| 金样档案群 | ✅ | `samples/persona-v1/` 00–07，已从旧单体迁移 |
| 旧管线归档 | ✅ | A/B 双产物、L1、单体档案迁入 `archive/reference/` |
| 问题库基础设施 | ✅ | 整理规范 v0.1、格式规范 v0.4、Builder、uid、registries |
| 首轮 categories | ✅ | StoryCorps P1 练手后 **209 题 active**；`Q-SELF-001` 保留 |

### 3.2 进行中

| 模块 | 状态 | 说明 |
| --- | --- | --- |
| P1 raw 整理 | 🔧 | McAdams / 口述史 / AAI 等待整理进 `categories/` |
| 查重机制 | 🔧 | `duplicates/` 文档就绪；首轮查重尚未跑 |

### 3.3 未开始

| 模块 | 说明 |
| --- | --- |
| 多用户实验 / 新中间层 | 旧 L1 中心流水线废止后，待实验再设计 |
| `generate_archive.py` | 从语料生成多文件档案群的自动化 |
| 动态追问规范 | 对话式发掘的正式契约 |
| 引擎闭环 | 架构草案见 [design/engine.md](design/engine.md)，未实施 |
| `question_guides/` · `analysis_guides/` | 本阶段明确不做 |

### 3.4 当前数据流

```text
L0 输入          samples/intake-v1.md（冻结）
       │
       ▼
档案文件群        samples/persona-v1/（§1 记录 + §2 解读 + §3 开放问题）
       ▲
问题地图          questions/categories/ ──mapsTo──► 02 维度地图 §14
```

历史中间层 `archive/reference/report-v1.md` 仅作参考，**不是活跃流水线**。

### 3.5 实现路径（路线图）

```text
① 输入金样      samples/intake-v1.md           ✅ 冻结
② 档案文件群    samples/persona-v1/            ✅ 金样完成，可持续迭代内容
③ 问题地图      questions/raw → categories/    🔧 Phase 1 整理中
④ 引擎闭环      PersonModel → 渲染多文件        ❌ 远期
⑤ Web 采集      表单 / 沉浸式皮肤               ❌ 远期
```

---

## 4. 仓库目录说明

```text
personal_archive/
├── README.md                      # 本文件 · 项目总入口
├── 项目状态.md                    # 阶段快照、进度表、建议操作（比本文件更细）
├── SYNC-CHECKLIST.md              # 改结构时的同步检查清单
├── 01-立意与分析体系.md            # ★ 宪法：立意、原则、文件架构、验收标准
├── 02-维度地图-dimensions.md       # ★ 认识论本体 §0–§14
│
├── samples/                       # 金样与输入（真实语料仅本地，见 samples/README.md）
│   ├── README.md                  # 隐私约定与本地目录说明
│   ├── intake-v1.md               # L0 手填语料（本地）
│   ├── intake-v1-clean.md         # 纯答案导出（本地）
│   └── persona-v1/                # 核心产出：8 文件档案群（本地）
│       ├── 00-总览与导航-overview.md
│       └── 01–07 各构成侧面
│
├── design/                        # 档案与引擎设计契约
│   ├── 00-档案文件群-index.md     # 阅读顺序、更新频率、与题库对应
│   ├── catalog/                   # 各侧面 §1/§2/§3 节标题模板
│   ├── intake-notes.md            # L0 输入相关设计笔记
│   ├── meta-frame-moment.md       # Frame / Moment 元数据语义
│   ├── skip-semantics.md          # 跳过 / 拒答语义
│   └── engine.md                  # 引擎架构草案（远期路线 ④）
│
├── questions/                     # 人物建档问题库
│   ├── README.md                  # 问题库入口与命令
│   ├── 整理规范-v0.1.md           # 整理阶段总规范（含批次验收 §21）
│   ├── schema/                    # 格式规范 v0.4 + JSON Schema
│   ├── registries/                # prerequisites / tags 标准库（yaml + md）
│   ├── categories/                # ★ 人类编辑的问题地图（209 active）
│   ├── raw/                       # 原始材料队列
│   │   ├── pending/               # 待整理（[Px] / [批次] / [元] 前缀）
│   │   └── processed/             # 已整理完成
│   ├── question_sources/          # 来源档案馆（卡片不移动，[状态][Px] 前缀）
│   ├── generated/                 # build_questions.py 编译产物（gitignore）
│   ├── duplicates/                # 查重报告
│   ├── rejected/                  # 淘汰题（含 system_unaskable）
│   ├── prompts/                   # 整理 / 查重 / registry 审核 Agent 提示词
│   ├── scripts/                   # build_questions.py 等
│   └── bank/ · canonical/         # 远期（500+ 题规模后）
│
├── prompts/                       # 全局 Prompt 目录（暂空；旧版在 archive）
├── experiments/                   # 多模型 L1 对比实验（历史方法验证）
│   ├── run_model_compare.py
│   └── archive/                   # AB intake 等历史实验
│
└── archive/                       # 历史版本，不描述当前架构
    ├── reference/                 # 旧 A/B 管线、L1、单体档案、废止设计契约
    └── questions-v1/              # 旧版题库骨架
```

---

## 5. 各功能区详解

### 5.1 根目录核心文档

| 文件 | 功能 | 何时读 |
| --- | --- | --- |
| **README.md**（本文件） | 项目总览、原则摘要、目录地图、当前状态 | 第一次了解项目；上下文有限的 AI |
| **[01-立意与分析体系.md](01-立意与分析体系.md)** | 宪法：立意、全部原则、文件架构、验收标准 | 做任何结构决策前 |
| **[02-维度地图-dimensions.md](02-维度地图-dimensions.md)** | 认识论：看人要哪些维度；§14 映射到文件群 | 设计引擎字段、题库 mapsTo、理解侧面覆盖 |
| **[项目状态.md](项目状态.md)** | 进度表、建议操作、给未来 AI 的注意事项 | 隔段时间回来、换模型、确认「现在做到哪了」 |
| **[SYNC-CHECKLIST.md](SYNC-CHECKLIST.md)** | 改哪些文件后要检查哪些关联项 | 修改宪法、维度、文件群结构、catalog 时 |

### 5.2 samples/ · 金样与输入

> **隐私**：真实 intake 与 persona 文件**不上传公开仓库**，仅本地保留。克隆后见 [samples/README.md](samples/README.md) 恢复或重建。

**`intake-v1.md`** — L0 层原始语料。手填问卷答案，含 `{}` 提问工程批注与 `<<>>` 分析批注。已冻结，是 `persona-v1/` 的主要证据来源。

**`persona-v1/`** — 当前唯一放「这个人」结构化档案的地方。8 个文件：

| 文件 | 侧面 | 典型内容 |
| --- | --- | --- |
| `00-总览与导航` | 入口 | 关键词、各文件 §2 核心句、语料索引 |
| `01-核心身份与画像` | 身份 | 基础事实、一句话画像、核心气质 |
| `02-性格与价值` | 性格 | 驱动力、价值排序、内在矛盾 |
| `03-认知与思维` | 认知 | 世界观、决策方式、思维习惯 |
| `04-关系世界` | 关系 | 家庭、亲密、友谊、边界 |
| `05-能力与爱好` | 能力 | 技能、兴趣、审美、生活习惯 |
| `06-人生轨迹` | 轨迹 | 经历时间线、转折、人物索引 → 链到 04 |
| `07-当下与未来` | 当下 | **唯一**写全「此刻」与近期张力；建档/追问后优先更新 |

每文件（除 00）内部结构：

- **§1** 原始记录与观察 — 只记录，不解释；缺料写「尚未记录」
- **§2** 当前解读与推断 — 须标〔推断〕与证据（intake 题号等）
- **§3** 待确认与开放问题 — 指引下一步发掘

**首次阅读路径**：`00-总览` → 按需打开 01–07，不必一次读完。

### 5.3 design/ · 设计契约

| 文件/目录 | 功能 |
| --- | --- |
| `00-档案文件群-index.md` | 阅读顺序、各文件何时打开、更新频率、questions 分类 → 档案文件对应表 |
| `catalog/` | 每个侧面的目录模板（节标题契约）；金样 `persona-v1/0x` 应与此对齐 |
| `intake-notes.md` | L0 输入层的设计笔记 |
| `meta-frame-moment.md` | 档案元数据：Frame（框架）与 Moment（时刻）语义 |
| `skip-semantics.md` | 用户跳过、拒答、「尚未记录」的处理约定 |
| `engine.md` | Person Archive Engine 架构草案：PersonModel、Processor 管道、插件协议（路线 ④，未实施） |

### 5.4 questions/ · 问题库

问题库**不是**心理测量库或诊断库；目标是通过提问**认识一个人**。量表、访谈、口述史都只是来源。

**数据流**：

```text
question_sources/     来源索引（卡片不移动）
raw/pending/          待整理原始材料
      ↓ 整理（Agent + 问题整理提示词）
categories/*.md       人类可编辑的问题地图（frontmatter + uid）
registries/*.yaml     prerequisites / tags 标准库
      ↓ build_questions.py
generated/*.json      questions.json · stats · duplicate_hints · registries 快照
      ↓ 查重
duplicates/           查重报告
raw/processed/        已处理 raw
rejected/             淘汰（含 system_unaskable：二元对话题）
```

**关键概念**：

| 概念 | 说明 |
| --- | --- |
| `uid` | 主键（8 位 hex）；`related` 与未来映射引用 uid |
| `id` | 人类编号如 `Q-SELF-001`；删题不重排 |
| `prerequisites` | 语义严格前提 — 无此事实则问题不成立 |
| `tags` | 主题检索标签 |
| `mapsTo` | 指向 02 维度地图细粒度坐标 |
| `system_unaskable` | 预设在场对话者（采访者↔被采访者）的题，不入 categories |

**整理 Agent 禁止读 02** — 分类与 mapsTo 由提示词与规范约束，避免维度本体污染整理过程。

**常用命令**：

```bash
python questions/scripts/build_questions.py
python questions/scripts/build_questions.py --audit-dyadic
python questions/scripts/build_questions.py --strict-registry
```

规范链：`整理规范-v0.1.md` → `schema/格式规范.md` → `registries/README.md` → `prompts/问题整理提示词.md`。

### 5.5 experiments/ · 实验

固定同一份 intake 语料 + 归档 L1 提示词，换不同 AI 模型，观察结论差异。**L1 管线已非活跃架构**；实验仅作历史方法验证，产出在 `experiments/outputs/`。

### 5.6 archive/ · 历史归档

**不描述当前架构。** 存放已废止的双产物（产物 A 分析报告 / 产物 B 人物档案）、L1 中间层、旧单体档案、废止的设计契约与脚本。查阅历史决策或对比迁移前后时可打开；日常工作以 `samples/persona-v1/` 为准。

索引：[archive/reference/README.md](archive/reference/README.md)。

---

## 6. 阅读指南

### 6.1 人类读者 · 5 分钟了解「这个人」

1. [samples/persona-v1/00-总览与导航-overview.md](samples/persona-v1/00-总览与导航-overview.md)
2. 按需扫 01–07 的 **§2**（当前解读）

### 6.2 人类读者 · 了解「这套体系」

1. 本 README
2. [01-立意与分析体系.md](01-立意与分析体系.md)
3. [design/00-档案文件群-index.md](design/00-档案文件群-index.md)
4. [02-维度地图-dimensions.md](02-维度地图-dimensions.md)（需要坐标时再读）

### 6.3 上下文有限的 AI · 最小必读集

若只能读少量文件，按此顺序：

1. **本 README** — 项目是什么、当前架构、目录地图、状态
2. **[01-立意与分析体系.md](01-立意与分析体系.md)** — 原则与文件架构（宪法）
3. **[项目状态.md](项目状态.md)** — 精确进度与当前建议操作

随后按任务追加：

| 任务 | 再读 |
| --- | --- |
| 阅读/更新金样人物 | `samples/persona-v1/00-总览` + 目标侧面文件 + 对应 `design/catalog/0x` |
| 整理问题 | `questions/README.md` + `整理规范-v0.1.md` + `prompts/问题整理提示词.md` |
| 改文件群结构 | `SYNC-CHECKLIST.md` + `02` §14 + `design/00-index` |
| 理解维度坐标 | `02-维度地图-dimensions.md` |

### 6.4 协作 AI · 启动顺序

1. [SYNC-CHECKLIST.md](SYNC-CHECKLIST.md)
2. [01-立意与分析体系.md](01-立意与分析体系.md)
3. [项目状态.md](项目状态.md)
4. 再修改任何结构或内容

**注意**：不要把 `{}` 批注当人格语料；当前产出是 **persona-v1/ 文件群**，不是 archive 里的产物 A/B。

---

## 7. 验收标准（档案群）

见 [01 §6](01-立意与分析体系.md)。摘要：

1. 陌生人读 00 + 各 §2，五分钟内能回答：他是谁、什么阶段、在意什么、如何与人相处、往哪走
2. 各文件 §3 有质量的开放问题，非空占位
3. 增删语料、修订 §2 不破坏三层结构与文件划分
4. 至少 2–3 条主题线跨文件 §2 互相印证
5. 核心维度 ≥60% 有 §1 记录；空缺写「尚未记录」

---

## 8. 文档索引（速查）

| 想了解什么 | 打开 |
| --- | --- |
| 项目原则与文件架构 | [01-立意与分析体系.md](01-立意与分析体系.md) |
| 精确进度与下一步 | [项目状态.md](项目状态.md) |
| 金样人物 | [samples/persona-v1/00-总览与导航-overview.md](samples/persona-v1/00-总览与导航-overview.md) |
| 看人要哪些维度 | [02-维度地图-dimensions.md](02-维度地图-dimensions.md) |
| 档案怎么读、怎么更新 | [design/00-档案文件群-index.md](design/00-档案文件群-index.md) |
| 某侧面的节标题契约 | [design/catalog/](design/catalog/) |
| L0 输入 | [samples/intake-v1.md](samples/intake-v1.md) |
| 问题库 | [questions/README.md](questions/README.md) |
| 改结构后的同步检查 | [SYNC-CHECKLIST.md](SYNC-CHECKLIST.md) |
| 历史管线与废止概念 | [archive/reference/README.md](archive/reference/README.md) |
| 引擎远期架构 | [design/engine.md](design/engine.md) |
