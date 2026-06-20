# 05-导入队列-Imports/ · 队列层

| 目录 | 说明 |
| --- | --- |
| [01-pending-待入库/](./01-pending-待入库/README.md) | Agent 输出的 jsonl，待 ingest |
| [02-processed-已入库/](./02-processed-已入库/README.md) | 成功归档 `*_ingested_<ts>.jsonl` |
| [03-failed-失败/](./03-failed-失败/README.md) | 失败文件 + `.error.log` |
| [04-external-外部工具/](./04-external-外部工具/README.md) | 第三方测评脚本，Agent 读后提炼 |

```bash
python questions/scripts/ingest.py
python questions/qcli.py ingest --stdin
```

**禁止** ingest 扫描 `01-文献与来源-Library/`。
