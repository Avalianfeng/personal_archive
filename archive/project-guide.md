# 项目指南：原则、验收与阶段

> **功能**：本仓库人物档案产品的总纲——稳定原则、「足够了解一个人」的验收标准、阶段路线与文档索引。  
> **定位**：面向产品设计与工程实现的单一入口；细节架构见 [person-archive-engine.md](./person-archive-engine.md)，阅读结构见 [archive-catalog-v1.md](../archive-catalog-v1.md)。  
> **状态**：V1 初稿  
> **关联**：[archive-catalog/](./archive-catalog/) · [persona-samples/](./persona-samples/) · [intake/](./intake/) · [../prompts/](../prompts/)

---

## 1. 项目原则

### 1.1 我们在做什么

构建 **Person Archive Engine**：把多种采集方式（表单、人格深潜、专项问卷）汇入统一档案模型，输出「像认识一个人」的详细报告——而不是问卷记录或测评结论。

### 1.2 稳定约束

1. **档案是关于人的，不是关于问题的。** 目录每一节回答「了解这个人」，而非「第几题放了什么」。
2. **建档优先于测评。** 正文不以「某某型人格」为主体；类型学标签仅可进附录作参考。
3. **详尽档案本体唯一。** [archive-catalog-v1.md](../archive-catalog-v1.md) §0–§13 描述「人」的完整阅读结构；技能、收入等 **专项插件外挂**，挂载相关三级条（如 §9），不替代主卷。
4. **简略从详尽中选取。** 简略模式是同一 PersonModel 的裁剪/摘要，不另建更短目录。
5. **设计顺序不可颠倒：**

```text
目录（读什么）→ 分析报告金样（写成什么样）→ Model 字段 → 题库分册 → Processor 提示词 → 引擎闭环 → Web 采集
```

6. **手填原版冻结。** [archive-intake-questionnaire-v1.md](./archive-intake-questionnaire-v1.md) 是 Persona 输入金样（含 `{}` 产品批注），不是上线题库。

### 1.3 输入 / 输出关系

| 文档 | 角色 |
| --- | --- |
| `archive-intake-questionnaire-v1.md` | 输入金样（原始语料 + 批注） |
| `persona-samples/person-analyze-report-v1.md` | 输出金样（分析初稿 → 用户定稿） |
| `intake/` 分册 | 优化后的采集题面（日后） |
| `prompts/` | 原话 → 档案语言的 Processor 提示词（日后） |

---

## 2. 「足够了解一个人」的验收标准

不追求完备，但须可检验。以下四层**全部满足**，即视为「足够出第一版详细报告」。

### 2.1 陌生人五问（阅读检验）

读完详细报告后，陌生人能**不靠猜**回答：

1. 这个人是谁、处在什么人生阶段？
2. 他最近最在意什么、压力从哪来？
3. 他看重什么、什么不能碰？
4. 他如何与人相处、在关系里是什么样？
5. 他往哪走、怕什么、期待什么？

对应 catalog 设计意图：§2、§5、§7、§12 等。

### 2.2 跨章一致性（叙述检验）

至少 **2–3 条主题线**在多处出现且可互相印证，而非互相矛盾。  
例：「对思考的依赖与不坚定」应能在处境、自我认知、决策等章节形成连贯读感。

### 2.3 三级条材料率（工程检验）

**「有材料」** = 有效自述 / 选项 / 插件汇入，且非「不想说 / 不要再问」。

| 门槛 | 建议值 | 含义 |
| --- | --- | --- |
| 核心章（§2、§4、§5、§7、§12） | ≥ 80% 三级条有材料 | 主干可写 |
| 全文 | ≥ 60% 三级条有材料 | 允许轨迹、底线等稀疏 |
| §13 综合 | 不需捏造重大事实 | 仅整理、推断语气 |

空缺条在报告中写「尚未记录」，不阻断发布。

### 2.4 快照诚实（档案检验）

报告须标明：**快照日期**、Frame 时间尺度（此刻 / 一贯 / 混合）、填写语境（Meta）。  
阶段性叙述与一贯叙述不得混写而不加说明。

### 2.5 首份 Persona 自评（示范）

基于 [archive-intake-questionnaire-v1.md](./archive-intake-questionnaire-v1.md) 手填完成情况（非打分，供对照）：

| 区块 | 材料情况 | 备注 |
| --- | --- | --- |
| §0 Meta | 完整 | Frame/Moment 已选 |
| §1 开篇 | 充实 | 1.1 已补；1.2 可由 Meta 生成 |
| §2–§4、§6–§7、§10–§12 | 充实 | 可支撑主干叙述 |
| §5 价值观 | 充实 | 5.5、5.6 已补 |
| §8 情感 | 充实 | 8.6 已补 |
| §9 能力 | 中等 | 学生向，专项技能日后可外挂 |
| §11 轨迹 | 有独特读法 | 「无单点转折」需档案语言转写 |
| 附录 A | 空 | 可选；A2 金句可日后由引擎摘录 |

**结论**：主文语料已满足第一版分析报告门槛；仅剩附录 A 可选。生成报告前见 [person-analyze-report-v1.md §待决事项](./persona-samples/person-analyze-report-v1.md#待决事项写正文前需确认)（人称、询问空间密度）。

---

## 3. 阶段路线

| Phase | 状态 | 内容 | 完成标志 |
| --- | --- | --- | --- |
| **0** | 完成 | 目录 V1 + 手填原版 | `archive-catalog-v1.md`、`archive-intake-questionnaire-v1.md` 定稿 |
| **1** | **待定** | `person-analyze-report-v1.md` | 分析写法商定 → AI 初稿（含询问空间）→ 用户二次定稿 |
| **2** | 未开始 | 分章讨论 → `docs/intake/` | 每章一册优化题面 + mapsTo 三级条 |
| **3** | 未开始 | `prompts/` 与 Processor | extract/synthesize 提示词对齐 catalog；金样报告反推 |
| **4** | 未开始 | 引擎最小闭环 | 导入答案 → PersonModel → 渲染至少一章 |
| **5** | 未开始 | Web 表单 | 采集皮肤；非当前瓶颈 |

Phase 1 暂缓原因：分析报告承载「分析体系」定稿，文体、询问空间、与目录的映射方式需单独讨论后再写。见 [persona-samples/README.md](./persona-samples/README.md)。

---

## 4. 文档索引

```text
archive-catalog-v1.md              # 理想档案目录（阅读契约）
docs/
├── project-guide.md               # 本文件
├── person-archive-engine.md       # 引擎架构
├── archive-report-spec.md         # P0 遗留对照
├── archive-intake-questionnaire-v1.md   # 手填输入金样
├── archive-catalog/               # Meta 等配套
├── persona-samples/               # 输入/输出金样
│   └── person-analyze-report-v1.md    # 待写：分析输出金样
├── intake/                        # 分册题库（占位）
prompts/                           # 分析提示词（占位）
plugins/core-intake/               # 当前 10 题插件（待收敛）
```

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| 0.1 | 2026-06-10 | 初稿：原则、验收四层、阶段路线、文档索引 |
