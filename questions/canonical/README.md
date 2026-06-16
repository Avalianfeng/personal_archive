# canonical · 标准题（暂不启用）

**状态**：预留目录，整理阶段第一轮**不启用**。

## 未来职责

当 `categories/` 中积累大量语义相近的变体后，在此归并为**唯一标准题**：

```text
Q-SELF-012、Q-SELF-088、Q-SELF-122  （categories，变体保留）
              ↓ 远期归并
C-SELF-004「他人误解」                 （canonical，标准题）
```

| 目录 | 职责 |
| --- | --- |
| `categories/` | 完整问题地图（允许重复、变体、多来源） |
| `canonical/` | 标准题（远期唯一表述） |

## 启用条件（全部满足后再考虑）

- [ ] 整理阶段第一轮完成（见 [整理规范-v0.1.md §十四](../整理规范-v0.1.md)）
- [ ] categories 达到 500+ 题
- [ ] duplicates 机制稳定运行
- [ ] 问题引擎设计启动

**不用** frontmatter `status: canonical` — 标准题身份由**本目录**表达。
