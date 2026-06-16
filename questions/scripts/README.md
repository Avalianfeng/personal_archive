# Question Builder · scripts

## build_questions.py（主入口）

```bash
python questions/scripts/build_questions.py
python questions/scripts/build_questions.py --audit-dyadic
python questions/scripts/build_questions.py --prune-dyadic   # 慎用：自动迁 dyadic 题
python questions/scripts/build_questions.py --dry-run --no-write-uid
```

### 产出（`generated/`，不提交 Git）

| 文件 | 内容 |
| --- | --- |
| `questions.json` | active + candidate 题目 |
| `stats.json` | 计数、id 空档、missing_uid |
| `duplicate_hints.json` | 完全重复 text |

### 行为

- 解析 `categories/*.md` frontmatter
- 缺失 `uid` → 自动生成 8 位 hex 并**写回 md**（默认开启）
- `--audit-dyadic`：列出疑似二元对话题
- **删题不重排 id**

### 依赖

Python 3.10+ · PyYAML（`pip install pyyaml`）

## parse_questions.py

薄 wrapper，调用 `build_questions.py`。

## archive/

已废弃的一次性脚本（如 `build_storycorps_p1.py`）。
