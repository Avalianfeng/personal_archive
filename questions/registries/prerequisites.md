# prerequisites · 前置条件标准库

> **含义**：**没有这个事实，问题就不存在** — 语义/指称层面的严格前提。
> **机器清单**：[prerequisites.yaml](./prerequisites.yaml)

---

## 克制原则（必读）

`prerequisites` **必须非常克制**。

### 唯一合法用途

只有当：

> **没有这个事实 → 这道题在语义上不成立**（指称失败、状态未发生、时空不存在）

才写 `prerequisites`。

### 不是 prerequisite 的情况

| 情况 | 处理 |
| --- | --- |
| 「没有 X 也能答」— 可答「从未」「不适用」「没有」 | **不写** prerequisite |
| 「感觉应该先确认一下」— 只是更贴切 | **不写**；用 tags 或引擎侧推荐 |
| 「问起来有点怪」— 社交不适 | **不写**；用户可自行跳过 |
| 「最好有相关经历再答」— 体验深度 | **不写** |
| 主题相关但非必要指称 | 用 `tags` |

**引擎默认**：未标注 prerequisite 的题**始终可呈现**；用户跳过即可。prerequisite 只在**已知事实为 false** 时帮引擎自动跳过，避免问出指称为空的句子。

### 判定口诀

读题干，想象被问者说：**「我没有 X。」**

- 若整道题变成**空问 / 指称不存在 / 逻辑上无法作答** → 可考虑 prerequisite
- 若仍可正常作答（含「从未有过」） → **不要**写 prerequisite

### 正反例

| 题干 | prerequisite？ | 理由 |
| --- | --- | --- |
| 你和**现任伴侣**最大的分歧是什么？ | ✅ `has_current_partner` | 无伴侣则「现任伴侣」指称不存在 |
| 成为**父母**后你最大的变化？ | ✅ `has_children` | 题面假定已为人父母 |
| 你的**职业生涯**中最大挑战？ | ❌ | 可答「我没有职业经历」 |
| **大学**时代最难忘的事？ | ❌ | 可答「没上过大学」 |
| 你的**信仰**如何影响决策？ | ❌ | 可答「我没有信仰」 |
| 你**参与政治**的经历改变过你吗？ | ❌ | 可答「我不参与政治」 |
| 你有兄弟姐妹吗？ | ❌ | 本题**建立**事实，不是消费事实 |

---

## prerequisites vs tags

| | prerequisites | tags |
| --- | --- | --- |
| 问的是 | **无此事实则问题不存在** | 题面涉及什么主题 |
| 严格度 | 极高，宁缺毋滥 | 可逐步补充 |
| 引擎 | 已知 false → 自动跳过 | 检索、组卷 |

**不要用 tag 代替 prerequisite**（也不要用 prerequisite 做主题过滤）。

---

## frontmatter 用法

```yaml
prerequisites:
  - has_current_partner
```

**默认**：省略 `prerequisites`（绝大多数题应如此）。

只有极少数题需要写。整理时**先过判定口诀**，不过则留空。

---

## 标准 id

完整列表见 [prerequisites.yaml](./prerequisites.yaml) — **不在此重复枚举**；yaml 随题库按需增长。

**新增 id**：同批写 yaml（`label` · `note` · `example`）+ frontmatter 引用 → **须过 [registry 审核](../prompts/registry审核提示词.md)**。

---

## 动态增长（开放世界）

**写不完，也不需要写完。** 人生指称不可枚举；yaml 是**索引**，不是百科全书。

| 目标 | 含义 |
| --- | --- |
| **引用完整** | 已入库题引用的 id 均在 yaml 登记 |
| **按需追加** | 新题带来新指称 → 同批追加 yaml + 引用 |
| **动态收敛** | 随整理迭代，`unknown_*` → 0 |

整理时**允许**动态追加条目，但：

1. 同一批次：`yaml 条目` + `题目 frontmatter` 一起产出
2. **必须**拉起 registry 审核子 Agent（见 [registry审核提示词.md](../prompts/registry审核提示词.md)）
3. 合并前 `build_questions.py --strict-registry`

---

## 粒度（中粒度优先）

| 粒度 | 示例 | |
| --- | --- | --- |
| 过粗 | `has_dependents` | ❌ |
| **适中** | `has_children` · `has_pets` · `has_siblings` | ✅ |
| 过细 | `has_golden_retriever` | ❌ 除非多题复用 |

现有 id 能覆盖 → **不新增**。仅当指称无法被任一已有 id 合理覆盖且通过克制原则时，新增中粒度 id。

---

## 与未来追问链

```text
「你有兄弟姐妹吗？」→ 事实仓库 has_siblings=true/false
        ↓
has_siblings=false → 跳过指称「兄弟姐妹」的题
has_siblings=true  → 可问「你和兄弟姐妹…」
```

`establishes: true` 表示：某题回答可**写入**事实仓库（引擎阶段实现）。

---

## 隐式前提

`can_understand_question` — 所有题默认，**不写入** frontmatter。

---

## 明确不做

- 不因「感觉应该包含前提」批量标注
- 不把 AAI 控场说明、研究目的写进 prerequisites
- 不用 prerequisites 替代用户跳过
