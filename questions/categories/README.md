# categories · 分类问题地图

**人类编辑源**。每题 YAML frontmatter 块，编译为 [generated/questions.json](../generated/questions.json)。

## 职责

- 问题地图 — 覆盖度优先
- 允许重复、变体、多来源
- **浏览轴**：按「这道题问什么」分文件
- **检索轴**：`tags` / `type` / `interaction`（见 [schema/格式规范.md](../schema/格式规范.md)）

## 格式

[schema/格式规范.md](../schema/格式规范.md) v0.2 · [问题整理提示词.md](../prompts/问题整理提示词.md)

改 md 后运行：

```bash
python questions/scripts/parse_questions.py
```

**勿用**单独一行的 `---` 作 Markdown 分隔线（会与 frontmatter 混淆）。

## 流向

```text
raw/ → 整理 Agent → categories/
     → parse_questions.py → generated/
     → 查重 → duplicates/
```

题目 `status: deprecated` 仍保留在 categories；**文件级**淘汰进 [rejected/](../rejected/README.md)。
