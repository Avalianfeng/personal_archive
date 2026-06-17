# generated/ · 审计层

**禁止手改**（`questions.json` · `stats.json` · `registries.json` 除外 — 这三者由 export 生成，部分入 Git 供 CI 对账）。

| 产物 | 说明 |
| --- | --- |
| `questions.json` | 引擎兼容导出（入 Git） |
| `stats.json` | 统计（入 Git） |
| `registries.json` | registry 快照 |
| `duplicate_report.md` | 查重嫌疑人 |
| `audit.log` | qcli/ingest 变更流水 |
| `.sync_manifest.json` | categories 同步哈希 |

刷新：`python questions/scripts/manage.py sync`
