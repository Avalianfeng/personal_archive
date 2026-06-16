# duplicates · 查重报告

查重 Agent 在 **categories/ 批量整理完成后** 输出的重复分析报告。本目录不存放题目正文。

## 职责

| 做 | 不做 |
| --- | --- |
| 按信息意图聚类 | 删除 categories 中的题 |
| 标注 `保留` / `重复候选` / `完全重复` | mapsTo / 维度映射 |
| 建议 cross-ref 更新 | 自动改写 categories |

## 用法

1. categories 积累一批题后，运行 [问题查重提示词](../prompts/问题查重提示词.md)
2. Agent 输出报告 Markdown，保存为 `report-YYYY-MM-DD.md`（或按批次命名）
3. 人类审阅后，将 `related:` / `status: deprecated` / `superseded_by` 写回 categories

## 三态定义

| 状态 | 含义 | 建议 |
| --- | --- | --- |
| **保留** | 信息意图不同 | 无需操作 |
| **重复候选** | 语义相近 | **全部保留**，更新 `related:` |
| **完全重复** | 同义同形 | 人类决定是否删一留一；删题进 rejected，不从此目录删 |

## 模板

见 [_template-report.md](./_template-report.md)。

## 关联

- [整理规范-v0.1.md §六、§七](../整理规范-v0.1.md)
- [categories/README.md](../categories/README.md)
