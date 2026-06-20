# 03-generated-审计产物/ · 审计层

**禁止手改**（由 sync/export 生成，部分入 Git）。**禁止**在 `03-规则与审计-Meta/` 下另建 `generated/` 目录——本目录为唯一审计产物真源。

| 分区 | 产物 |
| --- | --- |
| 调用区 | `questions.json` · `stats.json` · `registries.json` |
| 管理区 | `health.json` · [01-agent-Agent视图/](./01-agent-Agent视图/) |
| 审计 | `audit.log` · `.sync_manifest.json` |
| 清理期 | `duplicate_report.md` |

刷新：`python questions/scripts/manage.py sync`

Agent 读题：`qcli dump` 或 `01-agent-Agent视图/` — **不要**读 `02-问题地图-Views/`。
