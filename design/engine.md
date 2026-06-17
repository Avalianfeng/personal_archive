# 引擎架构(Person Archive Engine)

> **功能**:路线 ④「引擎闭环」阶段的架构单源真相——PersonModel、Processor 管道、插件协议。
> **定位**:立意与路线见 [01-立意与分析体系.md](../01-立意与分析体系.md);维度坐标见 [02-维度地图-dimensions.md](../02-维度地图-dimensions.md);阅读结构见 [design/00-档案文件群-index.md](./00-档案文件群-index.md);本文只管「怎么实现」。
> **代码**:`D:\personal_archive_code`(已移出本仓库,本阶段不动)。
> **历史**:P0–P2 的实现差距分析与 monorepo 重构清单已完成使命,见归档快照(git `43c6234` 前的 `docs/person-archive-engine.md`)。

---

## 1. 数据流

```text
原始表达 → 分题处理(Processor)→ 统一档案模型(PersonModel)→ 分块报告
```

反面教材(P0 已验证是错的):`问题 → 回答 → 直接写入报告`,产出的是问卷记录,不是人物档案。

**正反例**(职业题,用户答:「我是一名前端工程师,最近在考虑往产品方向发展,但还没有完全决定。」):

| 错误(直贴) | 正确(档案语言) |
| --- | --- |
| 职业:我是一名前端工程师,最近在考虑… | **职业发展** — 当前从事前端开发工作。近阶段开始关注产品设计与需求分析方向,处于探索职业拓展可能性的阶段。 |

## 2. PersonModel(统一档案模型)

```text
PersonModel
├── meta          # id, completeness, mode, updatedAt + Frame/Moment
├── objective     # 事实层:规范化字段 + 转写段落
├── personality   # 人格层:观察结论,非 raw 原话列表
├── modules       # 插件槽:personalityDive, skillSurvey, ...
└── audit         # 可选:原始回答追溯(附录,不进正文)
```

原则:

- 报告**只读 Model**,不读 raw answers;raw 仅 audit/附录
- 简单客观字段经 `normalize` 写入 objective
- 复杂回答经 `ai_extract` 写入 objective / personality
- 跨题/跨模块经 `ai_synthesize` 写入 personality 或合成节(§1.1、§13)
- 存储分 objective/personality,**阅读不分章**(同段可交织两层)

## 3. Processor 管道

每题配置(在 `plugins/*/processors.yaml`):

```yaml
id: career-main
layer: objective              # objective | personality
processor: ai_extract         # normalize | ai_extract | ai_synthesize
mapsTo: objective.career      # 对应档案目录三级条
options: [...]                # 锚点选项
allowFreeText: true           # 选项 + 补充输入框(默认题型)
promptRef: prompts/career-extract.md
```

| Processor | 输入 | 输出 | AI |
| --- | --- | --- | --- |
| `normalize` | 选项 / 短文本 | 枚举、格式、单位 | 否 |
| `ai_extract` | 选项 + 自由文本 | 结构化字段 + 档案语言段落 | 是 |
| `ai_synthesize` | 多题 / 模块 snapshot | 观察结论、综合段落 | 是 |

```text
输入插件 → RawAnswers → PerQuestionProcessor → MergeIntoModel → SectionSynthesizer → ReportRenderer
```

提示词约定见 [intake-notes.md](./intake-notes.md) 末节;具体内容以 `samples/report-v1.md` 定稿反推。

## 4. 输入插件体系

插件 = 一个纯文本目录:

```text
plugins/core-intake/
├── module.json           # id, name, uiExperience
├── questions.json        # 选项 + allowFreeText
├── processors.yaml       # 每题 processor
└── prompts/              # AI 提示词
```

| 类型 | UI 体验 | 说明 |
| --- | --- | --- |
| core-intake | `form` 整页表单 | 通用档案采集,测试基座 |
| personality-dive | `immersive` 逐题氛围 | 人格探索,15 维;完成后 `SessionSnapshot` → `modules.personalityDive` → synthesize 汇入相关章 |
| specialized-survey | `form` / `compact` | 技能、收入等,挂载 §9 等三级条,不并入主卷 |
| external-import | — | JSON 手动导入,预留 |

氛围 UI(粒子、音频)仅用于 immersive 类。问卷设计工具(插件工厂)排在最后:档案目录与 Processor 协议未稳定前不做。

**问题库导出**：`questions/generated/questions.json`（由 `export_json.py` 从 `question_registry` 生成）为引擎插件候选输入；整理阶段不做 mapsTo。日常维护用 `questions/qcli.py`。

## 5. 开放决策

- [ ] PersonModel 各字段最终清单(由档案目录三级条反推)
- [ ] archive-api 独立服务 vs 合并 personality-api
- [ ] 简略模式报告大纲
- [ ] 数据库路径约定
