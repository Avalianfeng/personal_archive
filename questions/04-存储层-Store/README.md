# 04-存储层-Store/ · 持久层

| 文件 | 说明 |
| --- | --- |
| `schema.sql` | DDL（入 Git） |
| `questions.db` | 运行层（gitignore） |

Bootstrap：

```bash
pip install -r requirements.txt
python questions/scripts/init_db.py
python questions/scripts/migrate_bootstrap.py
python questions/scripts/manage.py sync
```
