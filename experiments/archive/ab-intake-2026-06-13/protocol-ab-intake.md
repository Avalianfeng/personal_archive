# A/B 实验:纯答案 vs 答案+元认知批注

> **目的**:验证分析体系的**信息来源边界**——哪些结论只靠问卷答案就能推出,哪些必须依赖填写者的 `{}` / `<<>>` 元认知。
> **地位**:路线 ② 的实验分支;产出是**中间层分析报告**,不是最终展示报告。

---

## 三层文档(先对齐名称)

| 层 | 文件 | 给谁看 | 特征 |
| --- | --- | --- | --- |
| **L0 输入** | `samples/intake-v1.md`(冻结) / `intake-v1-clean.md`(导出) | 机器+分析者 | 题目+答案;可选批注 |
| **L1 中间层** | `experiments/report-v1-{A\|B}-*.md` | **你(体系构建者)** | 含原文引用、多解、置信度、分角度分析;可冗长、可矛盾 |
| **L2 展示层** | 日后 `report-display-v1.md`(未建) | 陌生人读者 | 干净叙述、像认识一个人;无〔推断〕、无开放问题 |

当前 `samples/report-v1.md` = **L1 的早期手工版 + 部分 L2 口吻**——第一版已经很好,但你的任务不是把它抛光成 L2,而是:**确认 L1 里哪些读法成立、哪些该保留为多解、哪些该删掉**。

---

## 版本定义

| 版本 | 输入 | 模型任务 |
| --- | --- | --- |
| **A(贫语料)** | [intake-v1-clean.md](../samples/intake-v1-clean.md) | 仅答案;不得引用 `{}`/`<<>>` |
| **B(富元认知)** | [intake-v1.md](../samples/intake-v1.md) | 答案为主;`{}`/`<<>>` 作填写者元认知,区分「自述」与「对体系的设计思考」 |

**同一套提示词骨架**:[prompts/full-report-v1.md](../prompts/full-report-v1.md),仅替换 `{INPUT_MODE}` 与 `{INTAKE_CONTENT}`。

---

## 运行步骤

1. 生成纯答案卷(若未生成):
   ```bash
   python experiments/make_intake_clean.py
   ```
2. 配置 API Key(DeepSeek):
   ```bash
   # 在 experiments/.env 或仓库根 .env
   DEEPSEEK_API_KEY=sk-...
   ```
3. 跑 A、B 各一次(建议同一模型、同一 temperature):
   ```bash
   python experiments/run_deepseek_report.py --variant A
   python experiments/run_deepseek_report.py --variant B
   ```
4. 填对比表:[compare-template.md](./compare-template.md)
5. **你只做一件事**:标记 A/B 与现有 `report-v1.md` 三方在**主题线**上的一致/分歧——一致=问卷可推;分歧=元认知或追问才出现。

---

## 对比时看什么(不是改文笔)

对每个**主题线**(不是每章),只问三句:

1. **A  alone 能否推出?** 能 → 该线应成为体系的「贫语料默认可达」
2. **B 是否显著加强?** 是 → 批注/元认知在体系里的权重规则是什么
3. **现有 report-v1 是否过度推断?** 是 → 在 L1 改回「多解」或删

建议优先对比的 5 条主题线(来自 report-v1 §13):

- 思考作为居所 / 保护思考的结构
- 渴望 + 低预期 双层结构
- 对思考的依赖与不坚定
- 价值「排序不了」/ 追求平和
- 关系居前 vs 社交孤立

---

## 与「逐题 prompt」的关系

本实验是**整卷一次读**——符合你现在的判断:上下文够时,先验证「全量分析提示词」能否产出可用 L1。

通过后,路线 ③ 再拆:

- 哪些段落必须 **synthesize 全卷** (§1.1、§13)
- 哪些可以 **extract 单条** (贫语料短答 + 追问)
- A/B 对比里「A 推不出、B 才推得出」的条目 → 标记为「需要元认知或追问」,不是「需要更长自述」

---

## 产出文件约定

```text
experiments/
├── report-v1-A-YYYYMMDD.md    # 版本 A 中间层
├── report-v1-B-YYYYMMDD.md    # 版本 B 中间层
├── compare-YYYYMMDD.md        # 对比表(你填)
└── notes-YYYYMMDD.md          # 体系结论(可选)
```

定稿后的 L1 裁判 → 再写 L2 展示层 prompt → 再拆 extract/synthesize 提示词。
