# raw · 原始问题堆积

来源混杂的原始输入区。只负责**把东西倒进来**，不要求分类、不要求 JSON。

## 用法

1. 复制量表、访谈、灵感、`intake` `{}` 批注等到新文件
2. 命名：`问题库-001.md`、`问题库-002.md` … 按批次递增
3. 在 [question_sources/](../question_sources/README.md) 登记来源卡片
4. 整理：Agent + [问题整理提示词.md](../prompts/问题整理提示词.md) → 输出到 `categories/`
5. 查重：积累一批后 + [问题查重提示词.md](../prompts/问题查重提示词.md) → `duplicates/`

## 整理后流向

| 结果 | 去向 |
| --- | --- |
| 可整理题目 | `categories/` |
| 损坏 / 残缺 / 错误复制 | `rejected/{文件名}-review.md` |
| 链接索引（非题目正文） | 迁入 `question_sources/`，不直接整理 |

**查重在 categories 之后**，不在 raw 阶段做。

## 模板

见 [问题库-001.md](./问题库-001.md)。

## 规范

整理阶段规则见 [整理规范-v0.1.md](../整理规范-v0.1.md)。整理 Agent **禁止读取** 02-维度地图。

## 备注

- `other_info.md` 为链接池，整理前先迁入 `question_sources/pending-links.md`
- 代码文件（如 `MBTI.js`、`big_five.ts`）整理时需抽取题目数组，非整文件入库
