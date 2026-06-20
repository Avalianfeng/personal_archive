# PVQ 整理实验 · 整理规范-v1.0 使用反馈



> **实验日期**：2026-06-17  

> **来源**：`01-文献与来源-Library/问题库-003.md`（Portrait Values Questionnaire，40 题）  

> **产出**：`05-导入队列-Imports/02-processed-已入库/PVQ-20260617_ingested_20260617T044358Z.jsonl`  

> **规范版本**：`questions/03-规则与审计-Meta/00-整理规范-v1.0.md`  

> **处置 commit**：`bc7603b`（文档/校验）· 第二轮优化（Agent 入口 · accept · dry-run）未单独 commit



---



## 处置总览（2026-06-17 对照 bc7603b）



| 类别 | 已解决 | 部分解决 | 未做 |

| --- | --- | --- | --- |

| §3 缺口与矛盾 | 6 | 0 | 0 |

| §4 操作摩擦 | 5 | 2 | 0 |

| §5 P0 | 4 | 0 | 0 |

| §5 P1 | 4 | 1 | 0 |

| §5 P2 | 2 | 0 | 1 → **11 已解决** |

| §6 提示词升级 | 1 | 0 | 0 |

| §7 建议增补章节 | 4 | 2 | 0 |



**结论**：反馈中的 **P0 与绝大多数 P1/P2 已在文档与代码层闭环**；剩余 3 项为体验/模板类，不影响再跑一批整理。



---



## 1. 实验摘要



| 步骤 | 结果 |

| --- | --- |

| 阅读规范链 | 整理规范-v1.0 → 问题整理提示词 → 分类原则 → 格式规范 → PVQ 卡片 → raw |

| jsonl 产出 | 40 行，`category: val`，`subcategory: 个人价值观`，`type: agreement`，`interaction: rating`，`source: PVQ` |

| 第三人称改写 | 全部 She→你；无 system_unaskable |

| `ingest.py` | **40 题入库**（Q-VAL-037 … Q-VAL-076） |

| 首跑阻塞 | `post_write_hooks` → `sync_categories.py` 因 `options` 为字符串数组崩溃 |

| 修正后验收 | `manage sync` ✓ · `duplicate_scan` 0 组 ✓ · `qcli doctor` OK ✓ |

| `05-导入队列-Imports/01-pending-待入库/` | 空（仅 README） |



**子分类决策**：`价值问题.md` 现有子分类（人生教训、人生目标、信仰与信念、底线与原则）均不适合整份量表；本批统一用 **`个人价值观`**，由 sync 自动写入 categories。



---



## 2. 整理规范-v1.0 好用之处



（实验观察，无需处置）



### 2.1 流程极简、可执行



§ Agent 整理产出 + § 批次验收四步命令，比旧版 raw→categories→build_questions 链短很多。Agent 只需写 jsonl、跑四条命令，职责边界（不负责 uid/id）清晰。



### 2.2 DB 时代禁止项明确



「禁止手改 categories」「禁止 ingest 扫描 source_library」两条在实验中直接避免了常见误操作；子分类通过 jsonl `subcategory` 字段自动 sync，本批新增「个人价值观」无需碰 md。



### 2.3 与卡片协作良好



`[待整理][P2] PVQ.md` 的整理注意（第三人称改写、agreement/rating、6 级锚点）与规范不冲突，足够完成本批。



### 2.4 批次验收清单可核对



§21 的「pending 为空」是硬指标，实验结束后可客观确认归档成功。



---



## 3. 缺口与矛盾



### 3.1 options 格式：三处不一致（**阻塞级**） — ✅ 已解决 `bc7603b`



| 文档 | 写法 | 处置 |

| --- | --- | --- |

| **整理规范-v1.0 示例** | 无 `options` 字段 | → §jsonl 字段契约 + PVQ 6 级示例 |

| **本实验任务说明示例** | 字符串数组 | → 提示词/规范已改为对象数组 |

| **`schema/question.schema.json`** | `{key,text}` 对象 | 未改 schema，与规范对齐 |

| **`sync_categories.py`** | 假定 `opt['key']` / `opt['text']` | 未改 sync，靠 ingest 校验拦截 |

| **`ingest.py` / `db.py`** | 曾接受字符串数组 | → `validate_options()` 入库前拒绝 |



### 3.2 问题整理提示词仍为 v0.4 / categories 时代 — ✅ 已解决 `bc7603b`



- 输出格式 → jsonl 每行示例

- 删除 build_questions / raw 主流程

- 批次验收链接 → `00-整理规范-v1.0.md §批次验收`



### 3.3 格式规范.md 未同步到 DB 时代 — ✅ 已解决 `bc7603b`



重写 Agent 契约节；删除 raw/build 主流程；增补 type/options/scale_note 对照表。



### 3.4 分类原则.md 链接旧版 — ✅ 已解决 `bc7603b`



链接改为 `00-整理规范-v1.0.md §来源优先级`。



### 3.5 type 命名：提示词 vs 卡片 vs schema — ✅ 已解决 `bc7603b`



整理规范 §type 与 options 表 + 量表 checklist 第 4 步给出决策。



### 3.6 ingest 失败时的恢复路径未文档化 — ✅ 已解决 `bc7603b`



整理规范 §失败恢复 + doctor `STALE`/`ERROR` 分流。



---



## 4. 操作摩擦（逐步记录）



| 步骤 | 摩擦 | 状态 |

| --- | --- | --- |

| 读规范 | v1.0 过短，需交叉读 4 份 | ✅ `04-prompts-Agent提示/01-整理Agent启动.md` 单页入口 |

| 写 jsonl | 任务示例曾给字符串数组 | ✅ ingest 现拒绝 + 文档已改 |

| 首跑 ingest | DB 写入后 sync 失败、文件已归档 | ✅ ingest 默认不 sync；`manage accept` 一键验收 |

| 修 options | 需读源码才知格式 | ✅ 规范 + validate_options 错误信息指向 §jsonl |

| 子分类 | 「个人价值观」无先例 | ✅ 分类原则已增例题 + 规范 §子分类命名 |

| tags | 宗教题是否加 `religion` tag | ✅ `整理Agent启动.md` §tags |

| 验收 | doctor drift 易误判整批失败 | ✅ `STALE:` vs `ERROR:` 分流 |



---



## 5. 具体改进建议



### P0（必须立即修） — 全部 ✅ `bc7603b`



| # | 建议 | 状态 | 落地位置 |

| --- | --- | --- | --- |

| 1 | 整理规范增补 jsonl 字段表 + options 示例 | ✅ | `00-整理规范-v1.0.md` §jsonl 字段契约 |

| 2 | 统一 options 示例为对象数组 | ✅ | 规范 · 提示词 · 格式规范 |

| 3 | 问题整理提示词升级 DB/jsonl 时代 | ✅ | `04-prompts-Agent提示/02-问题整理提示词.md` |

| 4 | ingest 入库前校验 options 形状 | ✅ | `scripts/db.py` `validate_options()` |



### P1（下一迭代）



| # | 建议 | 状态 | 落地位置 |

| --- | --- | --- | --- |

| 5 | 格式规范重写 Agent 契约 | ✅ | `02-schema-格式契约/01-格式规范.md` |

| 6 | 量表类来源整理 checklist | ✅ | `00-整理规范-v1.0.md` §量表类来源整理 checklist |

| 7 | 分类原则增加量表例题 | ✅ | `04-prompts-Agent提示/03-分类原则.md` 价值问题 · 个人价值观 |

| 8 | ingest 事务边界 | ⚠️ **部分** | §失败恢复 已写「只重跑 manage sync」；**未实现** sync 失败时 DB 回滚 |

| 9 | 修正 v0.1 交叉引用 | ✅ | 分类原则 · 提示词 · registry 审核提示词 |



### P2（体验优化）



| # | 建议 | 状态 | 落地位置 |

| --- | --- | --- | --- |

| 10 | 子分类命名指南 | ✅ | `00-整理规范-v1.0.md` §子分类命名 |

| 11 | source_library 卡片整理记录模板 | ✅ | `01-文献与来源-Library/README.md` §卡片模板 |

| 12 | doctor 区分 sync 未跑 vs 数据错误 | ✅ | `scripts/manage.py` `STALE:` / `ERROR:` |



---



## 6. 对 `问题整理提示词.md` 是否应同步升级 — ✅ 已解决 `bc7603b`



- 保留：去格式、system_unaskable、slug、type/interaction、翻译与残缺

- 重写：jsonl 输出、imports 流程、批次验收链接

- 整理员阅读笔记已追加 PVQ 实验条目



---



## 7. 规范本身建议增补的章节



| 建议章节 | 状态 | 落地 |

| --- | --- | --- |

| § jsonl 字段契约 | ✅ | `00-整理规范-v1.0.md` |

| § agreement 与 scale | ✅ | §type 与 options 表 |

| § 子分类策略 | ✅ | §子分类命名 |

| § 量表翻译 | ✅ | `整理Agent启动.md` §Portrait 改写 |

| § 失败恢复 | ✅ | §失败恢复 + `manage accept` |

| § 来源卡片回写 | ✅ | `01-文献与来源-Library/README.md` §卡片模板 |



---



## 8. 本实验统计



| 指标 | 值 |

| --- | --- |

| 入库 | 40 |

| 子分类 | 个人价值观（新增 1） |

| system_unaskable | 0 |

| 完全重复跳过 | 0 |

| candidate | 0 |

| tags | 0（全批省略） |

| id 范围 | Q-VAL-037 – Q-VAL-076 |



---



## 9. 结论（实验当时）



整理规范-v1.0 的 **DB 流程骨架正确且比旧流程轻量**，本批 PVQ 可在遵循 jsonl 契约的前提下完成入库与验收。  

**最大缺口是 options 格式与配套文档未对齐** — 已在 `bc7603b` 消除。



---



## 10. 后续优化处置（2026-06-17 第二轮）

| 方向 | 状态 | 落地 |
| --- | --- | --- |
| source_library 卡片模板 | ✅ | `01-文献与来源-Library/README.md` §卡片模板 |
| Agent 单页入口 | ✅ | `04-prompts-Agent提示/01-整理Agent启动.md` |
| ingest `--dry-run` | ✅ | `ingest.py` + `validate_ingest_record()` |
| 批次一键验收 | ✅ | `manage.py accept` |
| ingest 默认不 sync | ✅ | 解耦半成功态；`accept` 统一 sync |
| 量表 tags / 翻译模板 | ✅ | `整理Agent启动.md` |
| v0.1 规范废止标注 | ✅ | `整理规范-v0.1.md` |
| PVQ raw → processed | ✅ | `attachments/processed/问题库-003.md`；`[已整理][P2] PVQ.md` |
| post_write_hooks 回滚 | ⏸ 暂缓 | 默认不 sync 已足够；代码回滚 ROI 低 |

### 宏观管理（仍可演进，非阻塞）

| 方向 | 说明 |
| --- | --- |
| 来源索引页 | `01-文献与来源-Library/README.md` 汇总待整理/已整理 |
| pre-commit 捆绑 | dry-run + doctor 在提交前自动跑 |
| review → accept 联动 | review 批次结束后提示验收命令 |
| 其余 P1 卡片统一重命名 | McAdams 等整理完成后 `[待整理]`→`[已整理]` |

