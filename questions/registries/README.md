# registries · 标准字段仓库

> **v0.4** · 2026-06-16
> 机器可读：`*.yaml` · 人类说明：`*.md`

## 职责

| 仓库 | 回答什么 | 写入题目？ |
| --- | --- | --- |
| [prerequisites.yaml](./prerequisites.yaml) | **无此事实则问题不存在**（语义/指称严格前提） | 极少数题可选 `prerequisites:` |
| [tags.yaml](./tags.yaml) | **这道题关于什么主题？** 跨分类检索 | 可选 `tags:` |

**不是** mapsTo、不是推断、不是档案字段。

---

## 形状：索引，不是百科全书

**写不完，也不该试图写完。**

人生指称空间是开放的（代孕母亲、资助学生、死囚经历……）。试图在启动时枚举一切是过度工程（YAGNI），yaml 会膨胀且大量条目永无题引用。

**「尽量完全」的正确定义**：

> 对**当前已入库题库**：没有一道题引用未在 yaml 中登记的 id。
>
> 即 **引用完整性**，随题库增长**动态收敛** — 像索引跟书籍同步，而非提前编百科全书。

| 状态 | 含义 |
| --- | --- |
| 开放世界 | 未来新题可带来新 id |
| 引用完整 | 已有题引用的 id 必须已登记 |
| 按需增长 | 新题需要时才追加 yaml |
| 非必须清理 | 题删改后 orphan id 可保留，无害 |

Builder 的 `stats.json` → `unknown_prerequisites` / `unknown_tags` 即**引用完整性缺口**清单；`--strict-registry` 可阻断合并。

---

## 与三层边界

```text
questions/（问什么 + 成立条件）
    ↓ 未来
question_engine/（事实仓库 + prerequisites 检查 + 追问）
    ↓ 未来
analysis/（AI + 资料实时解读，非预置 analysis_guides  per 题）
    ↓
persona/（档案）
```

**本阶段不做**：`question_guides/` · `analysis_guides/` · 批量补全现有 209 题 metadata。

**prerequisites 克制原则**：只有「没有这个事实，问题就不存在」时才写。详见 [prerequisites.md](./prerequisites.md)。

---

## 扩展流程（整理时允许动态追加）

整理 Agent **可以**在同一批次中追加 `prerequisites.yaml` / `tags.yaml` 并引用 — **但必须过 registry 审核**。

```text
整理题面 → 发现需新 id
    ↓
主 Agent 起草 yaml 条目 + 题目 frontmatter
    ↓
拉起 registry 审核子 Agent（只读规范 + 现有 yaml）
    ↓
通过 → 一并提交 categories + registries
驳回 → 改用已有 id，或去掉 prerequisite/tag
    ↓
build_questions.py（建议 --strict-registry）
```

审核提示词：[prompts/registry审核提示词.md](../prompts/registry审核提示词.md)

**禁止**：在 frontmatter 引用未登记 id 且**不同批**补 yaml（会触发 unknown_*）。

---

## 粒度策略

| 粒度 | 示例 | 判断 |
| --- | --- | --- |
| 过粗 | `has_dependents` 覆盖子女+父母+宠物 | ❌ 丢失指称 |
| **适中** | `has_children` · `has_pets` · `has_siblings` | ✅ 默认目标 |
| 过细 | `has_golden_retriever` · `has_adopted_child_from_china` | ❌ 除非多题复用 |

**新增 prerequisite**：现有 id 无法合理覆盖 + 通过「我没有 X」测试 + 中粒度可复用。

**新增 tag**：现有 tag 无法检索覆盖 + 非事实前提 + 预期多题复用。

---

## Builder 校验

```bash
python questions/scripts/build_questions.py
python questions/scripts/build_questions.py --strict-registry   # 未知键报错
```

未知 id 默认写入 `stats.json` 警告；合并前建议 strict。

---

## 隐式前提

所有题目默认假定被问者具备基础理解能力（见 `prerequisites.yaml` → `implicit`）。**不必**每题写 `can_understand_question`。
