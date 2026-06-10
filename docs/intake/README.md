# 建档题库分册（占位）

> **功能**：按档案目录章节存放 **优化后的采集题面**（问法、控件、mapsTo），供日后收敛为 `plugins/core-intake/questions.json` 等。  
> **定位**：输入层设计文档；**不**复制 [archive-intake-questionnaire-v1.md](../archive-intake-questionnaire-v1.md) 手填原版（含批注者单独维护）。  
> **状态**：占位；待分章讨论后逐册填充  
> **关联**：[archive-catalog-v1.md](../../archive-catalog-v1.md) · [skip-semantics.md](./skip-semantics.md) · [project-guide.md](../project-guide.md)

---

## 分册索引

| 文件 | catalog | 说明 |
| --- | --- | --- |
| [00-meta.md](./00-meta.md) | §0 Meta | Frame / Moment 前置向导 |
| [01-opening.md](./01-opening.md) | §1 开篇 | 印象与阅读指引（部分可由 Meta/合成生成） |
| [02-situation.md](./02-situation.md) | §2 当下与处境 | |
| [03-profile.md](./03-profile.md) | §3 基础画像 | |
| [04-self.md](./04-self.md) | §4 自我认知 | |
| [05-values.md](./05-values.md) | §5 价值观与动机 | |
| [06-decision.md](./06-decision.md) | §6 决策与思考 | |
| [07-relationships.md](./07-relationships.md) | §7 人际关系 | |
| [08-emotion.md](./08-emotion.md) | §8 情感与内在世界 | |
| [09-capability.md](./09-capability.md) | §9 能力与经验 | 与技能专项插件衔接 |
| [10-lifestyle.md](./10-lifestyle.md) | §10 兴趣审美与生活方式 | |
| [11-trajectory.md](./11-trajectory.md) | §11 人生轨迹 | |
| [12-future.md](./12-future.md) | §12 未来与方向 | |

§13 综合观察 **无采集分册**（引擎 synthesize 生成）。附录 §A 见专项插件或可选补充题。

## 题面约定（草案）

- 每题须 `mapsTo` 到 catalog **三级条 ID**（如 `2.3.2`）
- 控件类型：choice / scale / text / ranked / multi-text（见手填卷 `{}` 批注）
- 跳过语义见 [skip-semantics.md](./skip-semantics.md)
