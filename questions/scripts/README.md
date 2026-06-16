# Question Builder · scripts

## build_questions.py（主入口）

```bash
python questions/scripts/build_questions.py
python questions/scripts/build_questions.py --audit-dyadic
python questions/scripts/build_questions.py --strict-registry
python questions/scripts/build_questions.py --prune-dyadic   # 慎用：自动迁 dyadic 题
python questions/scripts/build_questions.py --dry-run --no-write-uid
```

### 产出（`generated/`，不提交 Git）

| 文件 | 内容 |
| --- | --- |
| `questions.json` | active + candidate 题目 |
| `stats.json` | 计数、id 空档、missing_uid、registry 审计 |
| `duplicate_hints.json` | 完全重复 text |
| `registries.json` | prerequisites + tags yaml 快照（供引擎读取） |

### 行为

- 解析 `categories/*.md` frontmatter（含 `prerequisites`）
- 校验 `prerequisites` / `tags` 是否登记于 `registries/*.yaml`
- 未知 id 默认写入 `stats.json`；`--strict-registry` 则报错退出
- 缺失 `uid` → 自动生成 8 位 hex 并**写回 md**（默认开启）
- `--audit-dyadic`：列出疑似二元对话题
- **删题不重排 id**

### 依赖

Python 3.10+ · PyYAML（`pip install pyyaml`）

## parse_questions.py

薄 wrapper，调用 `build_questions.py`。

## archive/

**历史**一次性脚本（如 `build_storycorps_p1.py`）— **禁止用于新批次**。

新批次整理必须走 [问题整理提示词.md](../prompts/问题整理提示词.md) 逐题输出；bulk 灌库脚本只能归档参考，不得再跑。
