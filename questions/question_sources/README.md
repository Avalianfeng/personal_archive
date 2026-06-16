# question_sources · 问题来源索引

记录**未来发现的新来源**与现有 raw 材料的元信息。问题库永远不会完成，只会持续迭代。

## 用法

每发现一个来源，新增一张来源卡片（`.md`），包含：

| 字段 | 说明 |
| --- | --- |
| 名称 | 来源正式名称 |
| 类型 | 访谈 / 量表 / 口述史 / intake / 代码 / 链接 |
| 语言 | zh / en / 双语 / 粤语等 |
| raw 路径 | 对应 `raw/` 文件 |
| 整理优先级 | P1 / P2 / P3 |
| 状态 | 待整理 / 已整理 / rejected |
| 备注 | 抽取注意点、版权、残缺说明 |

## 原则

- 本目录是**索引**，不是题库；题目正文在 `raw/` 或整理后进入 `categories/`
- 链接池（如 `other_info.md`）应先在此登记，再决定是否抓取入 raw
- 不替代 [整理规范-v0.1.md](../整理规范-v0.1.md) 中的优先级规则

## 已知来源类型（持续扩展）

| 类型 | 示例 |
| --- | --- |
| 叙事访谈 | StoryCorps、McAdams Life Story、Southern Oral History |
| 关系访谈 | Adult Attachment Interview |
| 咨询 intake | 心理咨询、职业咨询（待收集） |
| 治疗叙事 | Narrative Therapy（待收集） |
| 量表 | PVQ、RSES、WHOQOL、Big Five、MBTI |
| 筛查 | PHQ-9、GAD-7（低优先级，入状态问题） |

## 索引

| 卡片 | 优先级 | 状态 |
| --- | --- | --- |
| [McAdams Life Story](./McAdams-Life-Story.md) | P1 | 待整理 |
| [StoryCorps Great Questions](./StoryCorps.md) | P1 | 待整理 |
| [Southern Oral History](./Southern-Oral-History.md) | P1 | 待整理 |
| [Adult Attachment Interview](./AAI-Protocol.md) | P1 | 待整理 |
| [50 Life Story Questions（博客版）](./50-Life-Story-Questions.md) | P1 | 待整理 |
| [PVQ 价值观量表](./PVQ.md) | P2 | 待整理 |
| [Rosenberg 自尊量表](./RSES.md) | P2 | 待整理 |
| [WHOQOL-100 香港版](./WHOQOL-HK.md) | P2 | 待整理 |
| [Big Five 大五人格](./Big-Five.md) | P3 | 待整理 |
| [MBTI 多套实现](./MBTI.md) | P3 | 待整理 |
| [待采集链接池](./pending-links.md) | — | 链接索引 |
| [raw 待 rejected 候选](./raw-rejected-candidates.md) | — | 待 review |
