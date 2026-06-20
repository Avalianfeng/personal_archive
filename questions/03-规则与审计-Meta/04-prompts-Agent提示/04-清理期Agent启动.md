# 清理期 Agent · 启动清单

> **阶段**：收集完成、进入「干净题库」收尾时启用。  
> **收集期不要读本文** — 整理 Agent 见 [01-整理Agent启动.md](./01-整理Agent启动.md)。

---

## 何时启用

- 各来源批次已 `[已整理]`，`05-导入队列-Imports/01-pending-待入库/` 长期为空
- 准备做：语义去重、量表代表题、subcategory 统一、quality 规则扫描

---

## 只读与工具

| 输入 | 路径 / 命令 |
| --- | --- |
| 全库 compact | `03-generated-审计产物/01-agent-Agent视图/bank_compact.md` 或 `qcli dump` |
| 本批 compact | `…/batch_delta_compact.md` 或 `qcli dump --batch` |
| 按类 compact | `…/by_category/{slug}.md` 或 `qcli dump -c val` |
| 机器查重 | `python questions/scripts/manage.py sync --with-duplicate-scan` → `03-generated-审计产物/duplicate_report.md` |
| 索引 | `…/bank_index.json` |
| 已知欠账 | `…/known_issues.md` |

| Agent 提示词 | 用途 |
| --- | --- |
| [05-问题查重提示词.md](./05-问题查重提示词.md) | 语义裁决 duplicate_report + compact |
| [06-问题审查提示词.md](./06-问题审查提示词.md) | 执行 `qcli relate` / `qcli edit` |

---

## 推荐流程

```bash
python questions/scripts/manage.py sync --with-duplicate-scan
# 查重 Agent → 建议命令
# 审查 Agent 或脚本批量：
python questions/qcli.py relate Q-XXX --similar-to Q-YYY
python questions/qcli.py edit Q-XXX --set status=deprecated
python questions/scripts/manage.py sync
python questions/qcli.py doctor
```

**待实现（清理期）**：`quality_scan.py`（leading、subcategory 规范、unaskable 复检）。

---

## 与项目立意

mapsTo / 维度地图对齐与 [`01-立意与分析体系.md`](../../01-立意与分析体系.md) 同步推进，不在收集期做。
