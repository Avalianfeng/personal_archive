# ai_extract 提示词

> **功能**：将单题或单条用户回答转为档案语言，写入 PersonModel 对应 `mapsTo` 字段。  
> **定位**：Processor Pipeline 第一层转写；简单字段可用 `normalize` 不经此目录。  
> **状态**：占位  
> **关联**：[../README.md](../README.md) · [person-archive-engine.md](../../docs/person-archive-engine.md) §3.3

---

## 单份模板结构（草案）

```markdown
# mapsTo: 2.2.1

## 输入
- 用户选项/原文
- meta.frame（语气）

## 任务
转写为第三人称观察句，1–3 句；不粘贴原话。

## 禁止
- 诊断标签、MBTI 型结论
- 编造输入中不存在的事实
```

## 待添加文件

按 catalog 三级条逐条添加；优先 §2、§4、§7（手填卷料足）。
