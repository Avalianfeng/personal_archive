# imports/ · 收件箱

| 目录 | 说明 |
| --- | --- |
| `pending/` | Agent 输出的 jsonl，待 ingest |
| `processed/` | 成功归档 `*_ingested_<ts>.jsonl` |
| `failed/` | 失败文件 + `.error.log` |
| `external/` | 第三方测评脚本，Agent 读后提炼 |

```bash
python questions/scripts/ingest.py
python questions/qcli.py ingest --stdin
```

**禁止** ingest 扫描 `source_library/`。
