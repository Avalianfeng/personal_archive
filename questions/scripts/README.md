# scripts · 题库工具

## parse_questions.py

将 `categories/*.md` 编译为 `generated/questions.json`。

```bash
# 从仓库根目录
python questions/scripts/parse_questions.py

# 或
cd questions/scripts && python parse_questions.py
```

### 依赖

- Python 3.10+
- PyYAML（`pip install pyyaml`）

### 校验

- `id` 全局唯一
- `category` 与文件 slug 一致
- `subcategory` 非空
- enum 字段合法

失败时非零 exit code。
