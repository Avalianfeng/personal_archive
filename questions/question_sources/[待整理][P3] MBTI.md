# MBTI · 多套实现

| 字段 | 值 |
| --- | --- |
| 类型 | 代码 / 量表 |
| 语言 | en |
| raw 路径 | 见下表 |
| 整理优先级 | **P3** |
| 状态 | 待整理 |

## raw 文件

| 文件 | 说明 |
| --- | --- |
| [[P3] MBTI.js](../raw/pending/%5BP3%5D%20MBTI.js) | 完整前端应用，**60 题** + UI；抽取 `MBTI.Data.questions` |
| [[P3] MBTI_2.ts](../raw/pending/%5BP3%5D%20MBTI_2.ts) | 经典 A/B 二选一，约 **70 题** |
| [[P3] MBTI_3.ts](../raw/pending/%5BP3%5D%20MBTI_3.ts) | MBTI + Big Five 混合 TypeScript |
| [[P3] MBTI_1.js](../raw/pending/%5BP3%5D%20MBTI_1.js) | 场景式多选题，带 dimension 分值 |

## 整理注意

- **不要**整文件入库；只抽取 `questions` 数组中的题干与选项
- 四套高度重叠，建议以 **MBTI_2.ts** 为主源，其余标 `[重复候选]`
- 题型：`单选` / `认同度`；`回答形式: rating` 或 `scenario`
- 按功能分散归类，**禁止** MBTI 四字母输出或类型推断
- P3 优先级：可在 P1/P2 完成后再处理

## 来源

标注 `来源: MBTI (实现名)`。
