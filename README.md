# Person Archive Engine

> **人的档案引擎** — 把原始表达经处理写入统一档案模型，再生成像「认识一个人」的报告。  
> 人格深潜（Personality Dive）是输入插件之一。

| 模块 | 说明 | 启动 |
| --- | --- | --- |
| **人格深潜** | 沉浸式人格探索 | `pnpm dev` 或 `pnpm dev:personality` |
| **个人档案** | 整页表单采集 → Markdown 报告 | `pnpm dev:archive` |

**设计文档**：[docs/person-archive-engine.md](docs/person-archive-engine.md)

---

## 核心原则

> **档案是关于人的，而不是关于问题的。**

```text
原始表达 → 分题处理 → PersonModel → 报告
```

---

## 目录结构

```text
personal_archive/
├── apps/
│   ├── personality/
│   │   ├── web/          # 人格深潜前端（immersive）  :5173
│   │   └── api/          # 人格深潜 API              :3001
│   └── archive/
│       └── web/          # 档案整页表单              :5174
├── packages/
│   ├── engine/           # 档案引擎核心
│   ├── personality/      # 人格维度与 scoring
│   └── plugin-sdk/       # 插件协议类型
├── plugins/
│   ├── core-intake/      # 通用档案问卷
│   └── personality-dive/ # 人格深潜题库
├── prompts/              # 引擎级提示词（P5+）
└── docs/
```

---

## 快速开始

```bash
pnpm install
```

### 人格深潜

```bash
cp apps/personality/api/.env.example apps/personality/api/.env
# 编辑 LLM_API_KEY

pnpm dev:personality
# web  http://localhost:5173
# api  http://localhost:3001
```

若根目录仍有旧 `.env`，可复制到新路径：

```bash
cp .env apps/personality/api/.env
```

### 个人档案

```bash
pnpm dev:archive
# http://localhost:5174
```

整页表单填写，每题可跳过，生成 Markdown 报告预览与下载。

---

## 文档

| 文档 | 说明 |
| --- | --- |
| [person-archive-engine.md](docs/person-archive-engine.md) | 主设计 — 架构、迁移、路线 |
| [archive-catalog-v1.md](archive-catalog-v1.md) | **理想人物档案目录 V1**（三级结构，初稿） |
| [docs/archive-catalog/](docs/archive-catalog/) | Frame / Moment 语境层草案 |
| [archive-report-spec.md](docs/archive-report-spec.md) | P0 报告格式（部分废弃） |
| [design-system.md](docs/design-system.md) | 人格深潜 immersive UI |
| [gpt.md](gpt.md) | 产品评审 |

---

## 开发阶段

| 阶段 | 状态 |
| --- | --- |
| P0 档案原型 | 已完成 |
| P1 设计文档 | 已完成 |
| P2 monorepo 重构 | 已完成 |
| P3 引擎 Processor 管道 | 待执行 |
| P4 AI 转写接入 | 待执行 |
| P5 archive-api | 待执行 |
| P6 人格深潜接入档案 | 待执行 |
| P7 问卷设计工具 | 规划中 |

---

## License

MIT
