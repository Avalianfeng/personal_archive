# external/

第三方测评脚本与采集工具（`.js` / `.ts` / Node 项目等）。Agent 读取后提炼题目 → `pending/`；采集工具输出 JSON/CSV 后同样走改写 → jsonl 流程。

不自动解析入库。

## 当前本地内容

| 路径 | 用途 | 来源卡片 |
| --- | --- | --- |
| `FreecramQuestionScraper/` | Freecram 考试页两阶段爬虫（Puppeteer） | [01-文献与来源-Library/[工具][P3] Freecram-Scraper.md](../../01-文献与来源-Library/[工具][P3]%20Freecram-Scraper.md) |
| `MBTI*.js/ts`、`big_five.ts` 等 | 测评脚本参考（按需放置） | 见 `01-文献与来源-Library/` 对应卡片 |

## FreecramQuestionScraper 快速启动

```bash
cd questions/05-导入队列-Imports/04-external-外部工具/FreecramQuestionScraper
npm install
npm start
```

抓取 JSON 建议保存到 `05-导入队列-Imports/01-pending-待入库/` 或 `01-文献与来源-Library/`，再经整理 Agent 转 jsonl。
