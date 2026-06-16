# tags · 主题标签标准库

> **含义**：**检索与组卷** — 题面涉及什么主题，不是事实前提。
> **机器清单**：[tags.yaml](./tags.yaml)

---

## tags vs 一级分类

| | category（文件） | tags |
| --- | --- | --- |
| 问的是 | 这道题**主要问什么**（功能分类） | **还涉及哪些主题**（跨类检索） |
| 例子 | 情感问题.md | `religion` + `family` |

**宗教 / 政治**：不单独开一级分类文件。按「问什么」归入现实/价值/自我认知/决策，用 tag 检索：

```yaml
# 家庭有宗教背景 → 现实问题
tags: [family, religion]

# 信仰对人生多重要 → 价值问题
tags: [religion, values]
```

---

## frontmatter 用法

```yaml
tags:
  - family
  - childhood
```

多数现有题**尚无 tags** — 正常。随整理逐步补充；须引用 [tags.yaml](./tags.yaml) 已登记 id。

---

## 动态增长（开放世界）

与 prerequisites 相同：**写不完，不追求写全**。

| 目标 | 含义 |
| --- | --- |
| **引用完整** | 已入库题引用的 tag 均在 yaml 登记 |
| **按需追加** | 整理时发现现有 tag 不够用 → 同批追加 yaml |
| **宁复用勿膨胀** | 优先用已有 tag；tag 门槛低于 prerequisite，但仍须审核 |

整理时**允许**动态追加 tag，**必须**过 [registry 审核提示词](../prompts/registry审核提示词.md)（子 Agent）。

完整列表见 [tags.yaml](./tags.yaml)。

---

## 明确不做

- 不用 tag 表达事实前提（用 `prerequisites`，且门槛更高）
- 不用 tag 做 mapsTo / 人格推断
- 不批量补全现有题库 tags
- 不为单题创造过细 tag（如 `storycorps_batch_3`）
