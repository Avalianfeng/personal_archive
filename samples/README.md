# samples/ · 本地金样（不上传公开仓库）

> **隐私约定**：本目录存放**真实人物**的 L0 输入与档案文件群，含可识别个人信息，**仅保留在本地**，已加入 `.gitignore`，不会进入公开 Git 历史的新提交。

---

## 目录结构（本地自行维护）

```text
samples/
├── README.md                 # 本说明（仓库内唯一跟踪文件）
├── intake-v1.md              # L0 手填语料（冻结）
├── intake-v1-clean.md        # 纯答案导出（实验 / 贫语料基线）
└── persona-v1/               # 当前金样档案群（8 文件）
    ├── 00-总览与导航-overview.md
    └── 01–07 各构成侧面
```

日后每人一个 `persona-<id>/`，结构同 `persona-v1/`。

---

## 各文件用途

| 文件 | 说明 |
| --- | --- |
| `intake-v1.md` | 手填问卷原版；含 `{}` 提问工程批注与 `<<>>` 个人旁白；**冻结不改** |
| `intake-v1-clean.md` | 由 intake 导出的纯题目+答案；可随脚本重生成 |
| `persona-v1/` | 结构化人物档案：每文件 §1 记录 + §2 解读 + §3 开放问题 |

侧面目录契约见 [design/catalog/](../design/catalog/)；阅读顺序见 [design/00-档案文件群-index.md](../design/00-档案文件群-index.md)。

---

## 新环境 / 新 Agent

1. 克隆公开仓库后，**本目录除 README 外为空**——需从本地备份恢复，或重新建档。
2. Agent 做金样相关工作时，先确认 `persona-v1/` 是否已在本地存在；不存在则只改 `design/`、`questions/` 等方法论部分。
3. 勿将真实 intake / persona 内容写入 commit。

---

## 相关本地路径（同样不上传）

| 路径 | 说明 |
| --- | --- |
| `archive/reference/report-v1.md` 等 | 旧管线 L1 / 单体档案快照 |
| `experiments/archive/ab-intake-2026-06-13/report-v1-*.md` | AB intake 实验报告 |
| `experiments/archive/ab-intake-2026-06-13/prompt-v1-*.md` | 含完整 intake 的实验 prompt |

方法论与 protocol 仍留在仓库；仅含真实语料的产出文件本地保留。
