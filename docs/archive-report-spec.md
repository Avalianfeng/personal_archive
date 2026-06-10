# 个人档案报告格式规范

> **状态：P0 遗留，部分设计已废弃。**  
> 架构与目标报告结构以 [person-archive-engine.md](./person-archive-engine.md) 为准（§2.1 理想档案目录）。  
> 本文档描述 **P0 实现** 的实际输出，供对照迁移；P3+ 将按新目录重写 `renderMarkdown`。

## 与目标架构的差异

| P0 本文档 | 目标（person-archive-engine） |
| --- | --- |
| 回答直写报告 / 原话列表 | Processor → PersonModel → 档案语言 |
| 章节：客观表 + 原始自述 | 章节：概览、人生状态、能力、价值观…（像认识一个人） |
| 选择或文本 | 选项 + 自由输入框 |
| 无 AI 处理 | normalize / ai_extract / ai_synthesize |

**废弃项**（勿在新代码中沿用）：

- 第四节「原始自述」作为报告正文
- [`mapAnswersToData`](../packages/engine/src/mapAnswers.ts) 直映射即最终档案
- 概览字段拼接（`displayName · age · city`）

**仍有效项**（迁移时可参考）：

- `mapsTo` 字段路径思路（将迁入 `processors.yaml`）
- `SynthesisGenerator` 接口扩展点
- 完整度计算公式（定义可能随「有效处理题数」调整）

---

## P0 报告章节树（当前实现）

> 单源实现：[`packages/engine/src/report/renderMarkdown.ts`](../packages/engine/src/report/renderMarkdown.ts)

| 章节 ID | Markdown 标题 | P0 内容来源 |
| --- | --- | --- |
| `overview` | 一、概览 | 模板拼接客观字段 |
| `objective_basic` | 二、基本信息 | `PersonArchive.data.basic` |
| `objective_social_career` | 三、社会与职业 | `data.social` + `data.career` |
| `inner_raw` | 四、内心与价值观 | 开放题原始答案列表 **（废弃）** |
| `synthesis` | 五、综合解读 | 占位（待 AI 生成） |

## P0 文档结构模板

```markdown
# 个人档案报告

> 生成时间：YYYY-MM-DD · 完整度：NN%

## 一、概览
...

## 二、基本信息
| 字段 | 内容 |
...

## 三、社会与职业
...

## 四、内心与价值观
### 原始自述
...

## 五、综合解读
> _本节待 AI 生成..._
```

## mapsTo 字段路径对照表（P0 题库）

| 问题 ID | mapsTo | 目标档案章节（P3+） |
| --- | --- | --- |
| `basic-name` | `basic.displayName` | 概览 / 生活环境 |
| `basic-age` | `basic.ageRange` | 当前人生状态 |
| `basic-location` | `basic.location` | 生活环境 |
| `social-relationship` | `social.relationshipStatus` | 关系与相处 |
| `social-circle` | `social.socialCircle` | 关系与相处 |
| `career-stage` | `career.careerStage` | 当前人生状态 |
| `career-occupation` | `career.occupation` | 能力与经验 |
| `inner-priority` | `inner.currentPriority` | 价值观与追求 |
| `inner-decision` | `inner.decisionStyle` | 决策方式 |
| `inner-notes` | `inner.additionalNotes` | 综合观察 / audit |

## 完整度计算（P0）

```
completeness = 已作答题数 / 总题数
```

## SynthesisGenerator 扩展点

```typescript
interface SynthesisGenerator {
  generate(archive: PersonModel): Promise<string>;
}
```

实现：[`StubSynthesisGenerator`](../packages/engine/src/report/synthesis.ts)

## 集成 TODO

- [ ] 人格深潜 `SessionSnapshot` → `PersonModel.modules.personalityDive`
- [ ] 报告按 [person-archive-engine.md §2.1](./person-archive-engine.md) 重写
- [ ] 综合解读 LLM 同时引用 objective + personality + modules

## 本地存储（P0 archive-web）

键名：`personal_archive_draft`（Zustand persist）
