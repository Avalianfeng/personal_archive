# Persona 金样（输入 / 输出）

> **功能**：存放「同一个人」的原始语料与目标分析报告，供题库、提示词、Renderer 对齐。  
> **定位**：金样层，不是上线数据、不是标准问卷。  
> **状态**：输入金样已完成；输出金样 **待商定写法**  
> **关联**：[project-guide.md](../project-guide.md) · [archive-intake-questionnaire-v1.md](../archive-intake-questionnaire-v1.md) · [archive-catalog-v1.md](../../archive-catalog-v1.md)

---

## 三者关系

| 文件 | 类型 | 说明 |
| --- | --- | --- |
| [archive-intake-questionnaire-v1.md](../archive-intake-questionnaire-v1.md) | **输入金样** | 完整手填原版：答案 + `{}` 产品批注 + `<<>>` 个人想法。**冻结，不改。** |
| [person-analyze-report-v1.md](./person-analyze-report-v1.md) | **输出金样** | 基于输入写的 **人物分析报告**（非 Q&A 清洗版） |
| （日后）`person-analyze-report-v1.final.md` | 定稿 | 用户二次修改后的分析体系定稿；可覆盖同文件 |

```text
手填原版（输入）  →  分析/处理  →  person-analyze-report（输出）  →  你修改  →  定稿
```

**不是输出金样的东西**：去掉批注、只留「问题 + 原话答案」的清洗卷——若需要可另立 `intake-clean` 类文件，优先级低于分析报告。

---

## person-analyze-report-v1.md 是什么（已定方向，写法待定）

- **结构**：对齐 catalog 读者可见 §1–§13；文首元信息（Frame/Moment 摘要、快照日期）
- **文体**：第三人称、观察式档案语言；连贯段落，非题号列表
- **语料**：以手填卷「答」与选项为主；`{}` / `<<>>` **不进正文**（产品批注另档留存）
- **询问空间**（初稿计划）：章末「待确认」、正文 `〔推断〕`、文末「开放问题」——供你二次修改，体现你的分析体系
- **当前状态**：仅占位；[待决事项](./person-analyze-report-v1.md#待决事项写正文前需确认) 已逐项说明；`{}` 附录一行索引 **已定**；主文空缺条（1.1、5.5、5.6、8.6）**已补**

---

## 使用方式

1. 讨论并确定 `person-analyze-report-v1.md` 写法规范  
2. AI 基于手填原版生成 V1 初稿（含询问空间）  
3. 你逐章修改 → 定稿成为 prompts / Renderer 的裁判文档  
4. 分章优化 `docs/intake/` 时，对照「输入问了什么」与「输出写成了什么」
