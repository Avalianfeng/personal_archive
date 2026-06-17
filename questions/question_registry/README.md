# question_registry/

Level 2 题目仓库（SQLite）。

| 文件 | 说明 |
| --- | --- |
| `schema.sql` | DDL（入 Git） |
| `questions.db` | 运行层（gitignore） |

## 新环境 bootstrap

```bash
pip install -r requirements.txt
python questions/scripts/init_db.py
python questions/scripts/migrate_bootstrap.py
python questions/scripts/sync_categories.py
python questions/scripts/export_json.py
```

默认从 `categories/*.md` 迁入；救急：`migrate_bootstrap.py --fallback-json generated/questions.json`。
