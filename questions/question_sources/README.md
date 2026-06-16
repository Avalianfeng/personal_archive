# question_sources · 问题来源索引

记录**来源元信息**与整理状态。问题库持续迭代，本目录是**档案馆**——卡片只改前缀、不移动文件夹。

## 一眼看懂：文件名即状态

```text
[状态][优先级] 卡片名.md     ← 来源卡片
[元] 描述.md                 ← 元索引（非来源卡片）
```

在资源管理器中按名称排序，**待办自然置顶**，无需打开文件。

### 状态前缀（来源卡片 · 必填）

| 前缀 | 含义 | 何时使用 |
| --- | --- | --- |
| `[待整理]` | raw 已入库，尚未进 categories | 默认状态；有 `raw/pending/` 对应文件 |
| `[待采集]` | 仅登记来源，raw 正文尚未抓取 | 链接池已确认、待复制入 raw |
| `[整理中]` | 正在执行整理 Agent | 人工临时标记，完成后改 `[已整理]` |
| `[已整理]` | raw 已提取进 categories | 对应 raw 应在 `processed/` |
| `[已拒绝]` | 决定不整理 | 残缺、版权、与项目定位不符 |

### 优先级后缀（来源卡片 · 必填）

紧跟状态后，与 [整理规范-v0.1.md](../整理规范-v0.1.md) 一致：

| 后缀 | 含义 |
| --- | --- |
| `[P1]` | 叙事 / 关系访谈、口述史 |
| `[P2]` | 价值观、自尊、生活质量等量表 |
| `[P3]` | 人格量表（Big Five、MBTI 等），信息增量低 |

无优先级时用 `[-]`（仅元索引）。

### 元索引前缀

| 前缀 | 含义 |
| --- | --- |
| `[元]` | 链接池、rejected 候选清单等**非来源卡片** |

## 卡片内容

每张来源卡片（`.md`）正文含：

| 字段 | 说明 |
| --- | --- |
| 名称 | 来源正式名称 |
| 类型 | 访谈 / 量表 / 口述史 / intake / 代码 / 链接 |
| 语言 | zh / en / 双语 / 粤语等 |
| raw 路径 | `raw/pending/` 或 `raw/processed/` 下对应文件（含优先级前缀） |
| 整理优先级 | P1 / P2 / P3（与文件名后缀一致） |
| 状态 | 与文件名前缀一致 |
| 备注 | 抽取注意点、版权、残缺说明 |

## 状态流转

```text
发现来源
  → 新建 [待采集][Px] 卡片.md（可选）
  → 抓取正文入 raw/pending/[Px] 文件名
  → 改卡片前缀为 [待整理][Px]
  → 整理 Agent → categories/
  → build_questions.py
  → raw 移入 processed/（文件名可去掉 [Px] 或保留）
  → 改卡片前缀为 [已整理][Px]
  → 残缺 / 不符 → rejected/ + 卡片改 [已拒绝][Px]
```

**规则**：改状态时**同步改文件名前缀**与卡片内「状态」字段；raw 路径链接一并更新。

## 原则

- 本目录是**索引**，不是题库；题目正文在 `raw/` 或整理后进 `categories/`
- 链接池先在 `[元] 待采集链接池.md` 登记，再决定是否抓取入 raw
- 不替代整理规范中的优先级规则

## 来源类型（持续扩展）

| 类型 | 示例 |
| --- | --- |
| 叙事访谈 | StoryCorps、McAdams Life Story、Southern Oral History |
| 关系访谈 | Adult Attachment Interview |
| 咨询 intake | 心理咨询、职业咨询（待收集） |
| 治疗叙事 | Narrative Therapy（待收集） |
| 量表 | PVQ、RSES、WHOQOL、Big Five、MBTI |
| 筛查 | PHQ-9、GAD-7（低优先级，入状态问题） |

## 索引（按状态分组）

### 元索引

| 文件 | 说明 |
| --- | --- |
| [[元] 待采集链接池](./[元]%20待采集链接池.md) | URL 清单，非题干 |
| [[元] rejected候选清单](./[元]%20rejected候选清单.md) | 待 review 的 raw |

### 待整理

| 文件 | 说明 |
| --- | --- |
| [[待整理][P1] McAdams-Life-Story](./[待整理][P1]%20McAdams-Life-Story.md) | 人生故事访谈 II |
| [[待整理][P1] Southern-Oral-History](./[待整理][P1]%20Southern-Oral-History.md) | 南方口述史 |
| [[待整理][P1] AAI-Protocol](./[待整理][P1]%20AAI-Protocol.md) | 成人依恋访谈 |
| [[待整理][P1] 50-Life-Story-Questions](./[待整理][P1]%2050-Life-Story-Questions.md) | 博客版 50 题 |
| [[待整理][P2] PVQ](./[待整理][P2]%20PVQ.md) | 价值观量表 |
| [[待整理][P2] RSES](./[待整理][P2]%20RSES.md) | Rosenberg 自尊 |
| [[待整理][P2] WHOQOL-HK](./[待整理][P2]%20WHOQOL-HK.md) | 香港生活质量 |
| [[待整理][P3] Big-Five](./[待整理][P3]%20Big-Five.md) | 大五 240 题 + TS |
| [[待整理][P3] MBTI](./[待整理][P3]%20MBTI.md) | 四套代码实现 |

### 已整理

| 文件 | 说明 |
| --- | --- |
| [[已整理][P1] StoryCorps](./[已整理][P1]%20StoryCorps.md) | Great Questions · 224 题入 categories |

规范：[整理规范-v0.1.md](../整理规范-v0.1.md) · [raw/README.md](../raw/README.md)
