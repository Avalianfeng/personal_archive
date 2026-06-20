# scripts/ · 工具层

| 脚本 | 用途 |
| --- | --- |
| `paths.py` | **路径真源**（所有目录常量） |
| `db.py` | 连接、write 内核、audit |
| `ingest.py` | `05-Imports` → `04-Store` |
| `sync_categories.py` | DB → `02-Views` |
| `export_json.py` | → `03-generated` |
| `export_agent_views.py` | → `03-generated-审计产物/01-agent-Agent视图` |
| `manage.py` | **`accept --json`** · `sync` · `check` |
| `pre_commit_check.py` | pre-commit 校验 |

日常操纵：[`../qcli.py`](../qcli.py)

历史脚本：[`99-archive-历史/`](./99-archive-历史/)
