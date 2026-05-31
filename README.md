# 人格深潜

> 通过最少的问题，逐步理解你的人格特征、价值观、行为模式与认知风格的 AI 探索系统。

## 技术栈

| 层 | 选型 |
| --- | --- |
| 仓库 | pnpm workspace monorepo |
| 前端 | React 18 + TypeScript + Vite + Tailwind CSS + Zustand + Framer Motion |
| 后端 | Fastify + better-sqlite3 + Zod |
| AI | OpenAI 兼容 API（默认 DeepSeek，可通过 .env 切换） |

## 快速开始

```bash
# 安装依赖
pnpm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 LLM_API_KEY

# 并行启动前后端
pnpm dev

# 或分别启动
pnpm dev:api   # http://localhost:3001
pnpm dev:web   # http://localhost:5173
```

## 项目结构

```
├── apps/
│   ├── web/          # Vite React 前端
│   └── api/          # Fastify 后端
├── packages/
│   └── shared/       # 共享类型与算法
├── docs/
│   └── design-system.md
└── .env.example
```

## License

MIT
