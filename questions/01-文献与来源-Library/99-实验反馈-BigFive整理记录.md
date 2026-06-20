# Big Five 整理实验 · 整理规范-v1.0 使用反馈

> **实验日期**：2026-06-17（验收 2026-06-18 UTC）  
> **来源**：`01-文献与来源-Library/问题库-001.md`（240 题陈述句）+ `05-导入队列-Imports/04-external-外部工具/big_five.ts`（成语版，仅查重参考）  
> **产出**：`05-导入队列-Imports/02-processed-已入库/BigFive-20260617_ingested_20260618T043307Z.jsonl`  
> **规范版本**：`questions/03-规则与审计-Meta/00-整理规范-v1.0.md` · 启动页 `04-prompts-Agent提示/01-整理Agent启动.md`

---

## 1. 实验摘要

| 步骤 | 结果 |
| --- | --- |
| 阅读链 | 整理Agent启动 → 整理规范-v1.0 → 问题整理提示词 → Big-Five 卡片 → 问题库-001 全文 |
| jsonl 产出 | **60 行**；`type: agreement` · `interaction: rating` · `source: Big Five (中文)` · 7 级 `{key,text}` options |
| 抽样策略 | 源 **#1,5,9…237**（步长 4，覆盖 240 题全段）；成语版 **未入库**；与 DB 无同形完全重复 |
| 归类 | **禁止** Big Five 维度作 subcategory；按「主要问什么」分散：`dec` 7 · `emo` 12 · `real` 9 · `self` 13 · `sta` 8 · `val` 11 |
| `ingest.py --dry-run` | **OK** — 60 record(s) |
| `manage.py accept` | **OK** — ingest 60 → sync → export → duplicate_scan → doctor |
| 入库题数 / id 范围 | **60 题**（**Q-DEC-006 … Q-VAL-087**） |
| duplicate_scan | **0** 组完全重复 |
| doctor | **OK** |
| `05-导入队列-Imports/01-pending-待入库/` | 空（仅 README） |
| pre-commit | `scripts/pre_commit_check.py` → categories check OK |

### 抽样逻辑说明

240 题信息增量有限（与既有 StoryCorps / PVQ 等 Portrait 题大量近义），卡片亦建议「可抽样 + 查重」。本批采用 **等距抽样（每 4 题取 1）** 而非按 N/E/O/A/C 维度分层，避免隐含人格维度目录。整理时对源文做了少量 OCR 修正（如 #97 断行合并、#105「别无他法」、#209 去掉尾部粘连「大五人格测验」）。**180 题未入库**；若后续需补量，可对剩余题再跑一轮步长 4 偏移抽样（#2,6,10…）并 duplicate_scan。

### 子分类分布（28 个，示例）

行事风格、计划性、情绪稳定、自制、社交偏好、情绪表达、自我欣赏与不足、底线与原则、社会观点、兴趣取向、生活方式 等 — 均由 jsonl `subcategory` 触发 sync，**未**使用开放性/尽责性等人格维度名。

---

## 2. 新基础设施：好用 / 摩擦

| 组件 | 体验 | 说明 |
| --- | --- | --- |
| **`01-文献与来源-Library/README.md`** | ✅ 好用 | P3 行一眼可见 Big Five 待办；实验后改 ✅ + 题数备注，与卡片 git mv 同步成本低 |
| **`04-prompts-Agent提示/01-整理Agent启动.md`** | ✅ 好用 | 单页 4 文件阅读序 + accept 命令；Big Five 无需 Portrait 改写表，但 7 级 options 契约在规范正文，启动页可再补一行 |
| **`ingest.py --dry-run`** | ✅ 好用 | 写 jsonl 后先 dry-run，60 题零错误再 accept；比 PVQ 时代「ingest 成功 sync 崩」安全 |
| **`manage.py accept`** | ✅ 好用 | 一条命令完成 ingest→sync→duplicate_scan→doctor；本批 **10s 内**闭环 |
| **`pre_commit_check.py`** | ✅ 无摩擦 | accept 后跑 categories check OK；与 doctor 互补 |
| **卡片模板 §整理记录** | ⚠️ 小摩擦 | 分散归类时「子分类」字段难填单一值；本批写「28 个子分类」+ 反馈文档，模板可加「多 subcategory 批次」示例 |

---

## 3. 规范 / 启动页 / 卡片：大五分散归类指导是否足够？

| 来源 | 结论 |
| --- | --- |
| **整理规范-v1.0 §来源优先级 P3** | 足够点明「分散入各类、信息增量有限」 |
| **分类原则.md** | 足够原则层；**缺** Big Five 陈述句 → category 的对照例题（如「我不是容易忧虑的人」→ `sta` 还是 `emo`？） |
| **Big-Five 卡片** | 足够禁止维度 subcategory；**建议增补**「7 级 Likert options 锚点」与「抽样 + 步长」示例（本批卡片已实验回写） |
| **问题整理提示词** | agreement + rating 清晰；P3 240 题 **未**写默认抽样规模，Agent 需读卡片「信息增量有限」自行决定 |

**总体**：完成本批 **足够**，但 P3 全量 240 题若再来一轮 Agent，**子分类命名会膨胀**（本批已 28 个 `##`）。规范可建议 P3 人格量表 **优先复用已有 subcategory**（如 `情绪稳定` 已有则勿新建近义 `抗压`）。

---

## 4. P3 · 240 题 scale 批次 workflow 建议

1. **主源择一**：问题库-001 陈述句；big_five.ts 永不 bulk ingest。  
2. **规模**：40–80 题 / 批；等距或功能分层抽样，**勿**按 N/E/O/A/C 分批。  
3. **options**：统一 7 级 `{key:"1"…"7", text:"非常不同意"…"非常同意"}`；与 PVQ 6 级「像我」区分写在卡片。  
4. **验收**：`dry-run` → `accept` → 回写卡片 + `_index` → 移 `attachments/processed/`。  
5. **剩余题**：卡片备注「已抽样 60/240」；下批用偏移抽样或 human 挑近义簇代表题。  
6. **duplicate_scan**：Portrait 量表与 Big Five 陈述句近义多，**0 组完全重复**不代表无检索重叠；可在反馈或卡片记「近义未 dedupe」。  

---

## 5. Top 3 改进建议

| 优先级 | 建议 | 理由 |
| --- | --- | --- |
| **P0** | **P3 卡片 + 启动页增补「7 级 agreement options 模板」** | 本批卡片写「认同度」但未给 key/text 锚点；Agent 需交叉读 PVQ 6 级再改 7 级，易与 schema 不一致 |
| **P1** | **分类原则增加「人格陈述句」例题表**（忧虑→sta/emo、狡猾→val、想象力→self…） | 分散归类是 P3 核心难点；本批 28 个子分类有合并空间（如「情绪体验」与「情绪表达」边界） |
| **P2** | **`_index.md` P3 行支持「部分整理」状态**（如 ✅ 60/240 抽样） | 240 题分多批时，索引仅 ✅/⏳ 二态不够表达进度；可在备注列写 `60/240 抽样`（本批已手动填写） |

---

## 6. 统计块（规范要求 · 本批）

- **各分类新增**：dec 7 · emo 12 · real 9 · self 13 · sta 8 · val 11  
- **related 标注**：0  
- **完全重复跳过**：0（抽样前未与 DB 同形重复）  
- **type: fill / candidate**：0  
- **validation**：0  
- **建议 rejected（raw）**：0  
- **system_unaskable**：0  
- **提醒**：已执行 `ingest.py --dry-run` → `manage.py accept`

---

## 7. 与 PVQ 实验对比

| 维度 | PVQ | Big Five |
| --- | --- | --- |
| 题数 | 40 全量 | 60 / 240 抽样 |
| subcategory | 单一「个人价值观」 | 28 个功能子类 |
| options | 6 级「像我」 | 7 级「同意」 |
| 第三人称改写 | 全部 She→你 | 源已为第一人称，无需 |
| 基础设施 | accept 已验证 | accept + dry-run + _index 再次验证 ✅ |

---

*本反馈供主 Agent / 人类排期下一批 P3（MBTI 或 Big Five 偏移抽样）参考。*
