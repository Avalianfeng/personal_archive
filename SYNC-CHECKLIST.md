# 项目同步检查清单

> **每个新开的 Agent 必须先读本文件。**
> 宪法：[01-立意与分析体系.md](01-立意与分析体系.md)
> 规则：修改下列任一文件后，按触发条件检查关联项。

---

## 新 Agent 启动顺序

1. 读 **本文件**（SYNC-CHECKLIST.md）
2. 读 [01-立意与分析体系.md](01-立意与分析体系.md)
3. 读 [项目状态.md](项目状态.md)
4. 再动任何结构或内容

---

## 核心文件（每次会话开始确认是否过期）

- [ ] [01-立意与分析体系.md](01-立意与分析体系.md)（宪法）
- [ ] [02-维度地图-dimensions.md](02-维度地图-dimensions.md)（本体论 + §14 映射）
- [ ] [项目状态.md](项目状态.md)（阶段、数据流、演变史）
- [ ] [README.md](README.md)（入口、快速命令）
- [ ] [design/00-档案文件群-index.md](design/00-档案文件群-index.md)（文件群契约）
- [ ] [design/catalog/*.md](design/catalog/)（各侧面目录）
- [ ] [questions/README.md](questions/README.md)（题库 → 档案文件对应）

---

## 触发规则

| 你改了什么 | 必须同步检查 |
| --- | --- |
| 宪法（01） | **全部**下游文件 |
| 维度地图（02）§14 映射 | `design/catalog/`、`questions/`、`samples/persona-v1/` 文件头 |
| 文件群结构（增删文件） | 01 §3、02 §14、00-index、项目状态、README |
| 单侧面目录（catalog） | 对应 `persona-v1/0x` 文件、02 §14 相关行 |
| 金样内容（persona-v1） | `00-总览-overview.md` 关键词与 §2 摘要 |
| 废弃/新增概念 | 01 §5、项目状态 §5 演变史、`archive/reference/` 索引 |

---

## 当前架构速记（勿与旧概念混淆）

| 概念 | 当前 | 已废止 |
| --- | --- | --- |
| 核心产出 | `samples/persona-v1/` 8 文件群（**本地金样**） | 单文件 `person-archive-v1.md` |
| 解读位置 | 各文件 §2 | 独立「产物 A 分析报告」 |
| 认识论坐标 | `02-维度地图-dimensions.md` | 02 兼作阅读契约 |
| 阅读顺序 | `design/00-档案文件群-index.md` | — |
| 中间层 | `archive/reference/report-v1.md`（历史） | L1 作为流水线中心 |

---

## 归档参考索引

历史管线与设计契约见 [archive/reference/README.md](archive/reference/README.md)。
