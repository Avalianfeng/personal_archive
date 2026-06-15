# personal_archive · 个人分析体系（文字仓库）

> 用「人物档案」作载体，表达并验证**我自己对人的分析体系与世界观**。
> 本仓库只放文字（立意、目录、金样、设计笔记）；代码在 `D:\personal_archive_code`。
>
> **新 Agent 必读** → [SYNC-CHECKLIST.md](SYNC-CHECKLIST.md) → [01-立意与分析体系.md](01-立意与分析体系.md) → [项目状态.md](项目状态.md)

---

## 当前位置

```text
宪法 01 + SYNC-CHECKLIST     ✅ 2026-06-15
多文件档案群 persona-v1/     ✅ 8 文件金样已迁移
维度地图 02 + design/catalog ✅
L0 输入 intake-v1            ✅ 冻结
旧 L1/A/B 管线               📦 archive/reference/
questions/ 问题库            🔧 raw → categories
动态发掘 / 生成脚本          ❌ 待多用户实验后
引擎 / Web                   ❌ personal_archive_code
```

---

## 快速入口

| 想了解什么 | 打开 |
| --- | --- |
| 项目是什么、原则、架构 | [01-立意与分析体系.md](01-立意与分析体系.md) |
| 这个人（金样） | [samples/persona-v1/00-总览与导航-overview.md](samples/persona-v1/00-总览与导航-overview.md) |
| 看人要哪些维度 | [02-维度地图-dimensions.md](02-维度地图-dimensions.md) |
| 档案文件怎么组织 | [design/00-档案文件群-index.md](design/00-档案文件群-index.md) |
| 阶段与演变 | [项目状态.md](项目状态.md) |

---

## 文档地图

| 文件 | 是什么 |
| --- | --- |
| [SYNC-CHECKLIST.md](SYNC-CHECKLIST.md) | **同步检查清单**（新 Agent 先读） |
| [01-立意与分析体系.md](01-立意与分析体系.md) | 宪法：立意、原则、文件架构 |
| [02-维度地图-dimensions.md](02-维度地图-dimensions.md) | 认识论本体 §0–§14 |
| [design/00-档案文件群-index.md](design/00-档案文件群-index.md) | 阅读顺序与文件群契约 |
| [design/catalog/](design/catalog/) | 各侧面目录模板 |
| [samples/persona-v1/](samples/persona-v1/) | **金样档案文件群** |
| [samples/intake-v1.md](samples/intake-v1.md) | L0 输入（冻结） |
| [questions/README.md](questions/README.md) | 问题库 |
| [archive/reference/](archive/reference/) | 旧管线与设计契约 |
| [experiments/](experiments/) | 多模型 L1 对比（历史 prompt） |

---

## 数据流（当前）

```text
intake-v1 (L0, 冻结)
       │
       ▼
persona-v1/ (8 文件档案群：§1 记录 + §2 解读 + §3 开放问题)
       ▲
questions/categories/ ──mapsTo──► 02 维度地图 §14
```

历史中间层 `archive/reference/report-v1.md` 仅供参考，非活跃流水线。

---

## 代码仓库

`D:\personal_archive_code` — 人格深潜、引擎骨架。设计以 [design/engine.md](design/engine.md) 为准。
