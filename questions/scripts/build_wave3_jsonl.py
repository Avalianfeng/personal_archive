#!/usr/bin/env python3
"""Build Wave 3 pending jsonl: WHOQOL, MBTI, MMDI, lifeintquestions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "01-文献与来源-Library"
PENDING = ROOT / "05-导入队列-Imports" / "01-pending-待入库"
EXTERNAL = ROOT / "05-导入队列-Imports" / "04-external-外部工具"
DATE = "20260620"

WHOQOL_OPTIONS = [
    {"key": "1", "text": "完全不符合"},
    {"key": "2", "text": "少许符合"},
    {"key": "3", "text": "某种程度符合"},
    {"key": "4", "text": "很大程度符合"},
    {"key": "5", "text": "完全符合"},
]

TRAD_PAIRS = [
    ("擔", "担"), ("覺", "觉"), ("過", "过"), ("經", "经"), ("麼", "么"), ("發", "发"),
    ("對", "对"), ("會", "会"), ("來", "来"), ("這", "这"), ("還", "还"), ("為", "为"),
    ("與", "与"), ("從", "从"), ("無", "无"), ("時", "时"), ("應", "应"), ("該", "该"),
    ("體", "体"), ("關", "关"), ("開", "开"), ("問", "问"), ("讓", "让"), ("類", "类"),
    ("種", "种"), ("處", "处"), ("環", "环"), ("節", "节"), ("運", "运"), ("動", "动"),
    ("費", "费"), ("價", "价"), ("長", "长"), ("見", "见"), ("認", "认"), ("識", "识"),
    ("說", "说"), ("話", "话"), ("請", "请"), ("讀", "读"), ("書", "书"), ("寫", "写"),
    ("國", "国"), ("學", "学"), ("業", "业"), ("產", "产"), ("專", "专"), ("區", "区"),
    ("縣", "县"), ("東", "东"), ("車", "车"), ("電", "电"), ("風", "风"), ("氣", "气"),
    ("錢", "钱"), ("買", "买"), ("賣", "卖"), ("視", "视"), ("聽", "听"), ("聲", "声"),
    ("願", "愿"), ("難", "难"), ("舊", "旧"), ("師", "师"), ("醫", "医"), ("療", "疗"),
    ("藥", "药"), ("獨", "独"), ("歡", "欢"), ("樂", "乐"), ("離", "离"), ("雖", "虽"),
    ("雙", "双"), ("務", "务"), ("員", "员"), ("場", "场"), ("廠", "厂"), ("廣", "广"),
    ("門", "门"), ("間", "间"), ("裡", "里"), ("內", "内"), ("細", "细"), ("組", "组"),
    ("結", "结"), ("絕", "绝"), ("給", "给"), ("線", "线"), ("繼", "继"), ("續", "续"),
    ("練", "练"), ("綠", "绿"), ("網", "网"), ("總", "总"), ("義", "义"), ("習", "习"),
    ("聯", "联"), ("聖", "圣"), ("極", "极"), ("歷", "历"), ("歲", "岁"), ("壓", "压"),
    ("擾", "扰"), ("憂", "忧"), ("慮", "虑"), ("積", "积"), ("極", "极"), ("經", "经"),
    ("歷", "历"), ("睏", "困"), ("擾", "扰"), ("約", "约"), ("束", "束"), ("憂", "忧"),
    ("鬱", "郁"), ("藥", "药"), ("醫", "医"), ("療", "疗"), ("滿", "满"), ("環", "环"),
    ("境", "境"), ("護", "护"), ("極", "极"), ("嗎", "吗"), ("麼", "么"), ("於", "于"),
    ("當", "当"), ("將", "将"), ("帶", "带"), ("條", "条"), ("標", "标"), ("準", "准"),
    ("實", "实"), ("際", "际"), ("顯", "显"), ("現", "现"), ("經", "经"), ("驗", "验"),
]


def trad2simp(text: str) -> str:
    t = text.replace(" ", "").replace("\u3000", "")
    t = re.sub(r"\(cid:[^)]+\)", "", t)
    t = re.sub(r"□\(cid:\d+\)", "", t)
    t = re.sub(r"□", "", t)
    for a, b in TRAD_PAIRS:
        t = t.replace(a, b)
    t = re.sub(r"\s+", "", t)
    t = t.replace("自已", "自己")
    return t.strip()


def whoqol_subcategory(q: str) -> str:
    keys_body = ("痛", "疲", "睡眠", "病", "健康", "药物", "医疗", "器材")
    if any(k in q for k in keys_body):
        return "疾病与身心"
    return "近期状态"


def extract_whoqol() -> list[dict]:
    text = (LIB / "09-WHOQOL-正文-Cantonese-QOL112.md").read_text(encoding="utf-8")
    questions: list[str] = []
    seen: set[str] = set()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("| ---"):
            continue
        if line.startswith("|") and ("你" in line or "你" in line):
            cells = [c.strip() for c in line.split("|") if c.strip()]
            joined = "".join(cells)
            joined = re.sub(r"^\d+\.?", "", joined)
            joined = re.sub(r"F[\d.]+", "", joined)
            q = trad2simp(joined)
            if q.endswith("？") or q.endswith("?"):
                q = q.rstrip("?") + "？"
            elif "吗" not in q and "？" not in q:
                if re.search(r"[吗嗎]$", joined):
                    q += "？"
                else:
                    continue
            if len(q) < 6 or "你" not in q:
                continue
            if q not in seen:
                seen.add(q)
                questions.append(q)
            continue
        cleaned = trad2simp(line)
        m = re.search(r"你[^？?]{2,120}[吗嗎]？", cleaned)
        if m:
            q = m.group(0)
            if q not in seen:
                seen.add(q)
                questions.append(q)

    records = []
    for q in questions:
        sub = whoqol_subcategory(q)
        status = "candidate" if re.search(r"[\(（].*[\)）]", q) or len(q) > 80 else "active"
        records.append(
            {
                "question": q,
                "category": "sta",
                "subcategory": sub,
                "type": "agreement",
                "interaction": "rating",
                "source": "WHOQOL",
                "status": status,
                "options": WHOQOL_OPTIONS,
            }
        )
    return records


def extract_mbti() -> list[dict]:
    src = (EXTERNAL / "MBTI_2.ts").read_text(encoding="utf-8")
    blocks = re.findall(
        r'question:\s*"([^"]+)"\s*,\s*answerOptions:\s*\[(.*?)\]',
        src,
        re.DOTALL,
    )
    translations = {
        "At a party do you: ": "在派对上，你更倾向于：",
        "Are you more: ": "你更偏向：",
        "Is it worse to: ": "哪一种更糟：",
        "Are you more impressed by: ": "你更容易被什么打动：",
        "Are more drawn toward the: ": "你更容易被什么吸引：",
        "Do you prefer to work: ": "你更喜欢的工作方式是：",
        "Do you tend to choose: ": "你做选择时通常：",
        "At parties do you: ": "在派对上，你通常：",
        "Are you more attracted to: ": "你更容易被哪种人吸引：",
        "Are you more interested in: ": "你更感兴趣的是：",
        "In judging others are you more swayed by: ": "评判他人时，你更受什么影响：",
        "In approaching others is your inclination to be somewhat: ": "接近他人时，你倾向于：",
    }
    answer_zh = {
        "Interact with many, including strangers": "与很多人互动，包括陌生人",
        "Interact with a few, known to you": "与少数熟人互动",
        "Realistic than speculative": "务实而非空想",
        "Speculative than realistic": "空想而非务实",
        'Have your "head in the clouds"': "想入非非",
        'Be "in a rut"': "墨守成规",
        "Principles": "原则",
        "Emotions": "情感",
        "Convincing": "有说服力",
        "Touching": "打动人心",
        "To deadlines": "按截止日期",
        'Just "whenever"': "随性而为",
        "Rather carefully": "相当谨慎",
        "Somewhat impulsively": "有些冲动",
        "Stay late, with increasing energy": "待到很晚，越待越有精神",
        "Leave early with decreased energy": "较早离开，精力递减",
        "Sensible people": "务实的人",
        "Imaginative people": "富有想象力的人",
        "What is actual": "实际的东西",
        "What is possible": "可能的东西",
        "Laws than circumstances": "法则而非情境",
        "Circumstances than laws": "情境而非法则",
        "Objective": "客观",
        "Personal": "个人化",
    }

    records = []
    for q_en, opts_block in blocks:
        q_prefix = translations.get(q_en)
        if not q_prefix:
            stem = q_en.strip().rstrip(": ")
            q_prefix = f"请二选一：{stem}"
        opts = re.findall(r'answer:\s*"([^"]+)"', opts_block)
        if len(opts) < 2:
            continue
        q_text = q_prefix if q_prefix.endswith("？") else q_prefix.rstrip(": ") + "？"
        options = [
            {"key": "A", "text": answer_zh.get(opts[0], opts[0])},
            {"key": "B", "text": answer_zh.get(opts[1], opts[1])},
        ]
        q_lower = q_en.lower()
        if any(w in q_lower for w in ("party", "energy", "others", "approaching")):
            cat, sub = "emo", "社交偏好"
        elif any(w in q_lower for w in ("work", "choose", "deadline", "impuls")):
            cat, sub = "dec", "行事风格"
        elif any(w in q_lower for w in ("judge", "principle", "emotion", "convincing")):
            cat, sub = "val", "底线与原则"
        else:
            cat, sub = "self", "思维方式"
        records.append(
            {
                "question": q_text,
                "category": cat,
                "subcategory": sub,
                "type": "single",
                "interaction": "scenario",
                "source": "MBTI (MBTI_2)",
                "status": "active",
                "options": options,
            }
        )
    return records


def extract_mmdi() -> list[dict]:
    raw = (LIB / "11-MMDI-多相人格量表.md").read_text(encoding="utf-8")
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    pairs: list[tuple[str, str]] = []
    for ln in lines:
        if "空白间隔物" in ln or ln.startswith("©") or "请输入" in ln or "兴趣点" in ln:
            continue
        if any(x in ln for x in ("梅塔拉萨", "MMDI", "说明：", "Cookie", "个性页面", "心理肌肉")):
            continue
        if "。" in ln and len(ln) > 15:
            parts = [p.strip() for p in re.split(r"[。．]", ln) if len(p.strip()) > 6]
            if len(parts) >= 2:
                for i in range(0, len(parts) - 1, 2):
                    pairs.append((parts[i] + "。", parts[i + 1] + "。"))

    records = []
    seen_pairs: set[str] = set()
    for a, b in pairs:
        key = a + b
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        q = "以下哪一句更像你？"
        full_q = f"{q} A）{a} B）{b}"
        if "价值" in a + b or "信念" in a + b or "规则" in a + b:
            cat, sub = "val", "底线与原则"
        elif "Feel" in a or "感受" in a + b or "关系" in a + b or "冲突" in a + b:
            cat, sub = "emo", "情绪体验"
        elif "计划" in a + b or "组织" in a + b or "程序" in a + b:
            cat, sub = "dec", "计划性"
        elif "思考" in a + b or "理论" in a + b or "逻辑" in a + b:
            cat, sub = "self", "思维方式"
        else:
            cat, sub = "dec", "行事风格"
        records.append(
            {
                "question": full_q,
                "category": cat,
                "subcategory": sub,
                "type": "single",
                "interaction": "rating",
                "source": "MMDI",
                "status": "active",
                "options": [{"key": "A", "text": a}, {"key": "B", "text": b}],
            }
        )
    return records


LIFE_TRANSLATIONS: dict[str, str] = {}


def _life_q(en: str) -> str:
    mapping = {
        "What year were you born? On what date? What day of the week was it? Did your parents tell you anything about the day you were born?":
            "你是哪一年、哪一天出生的？星期几？父母曾告诉过你关于出生那天的什么事吗？",
        "Where were you born?": "你在哪里出生？",
        "Why were you given the first (and middle) name(s) that you have?":
            "父母为什么给你取现在的名字（含中间名）？",
        "What's your first, most vivid memory?": "你最早、最鲜明的记忆是什么？",
        "What was the apartment or house like that you grew up in? How many bedrooms did it have? Bathrooms? What was your bedroom like?":
            "你小时候住的房子或公寓是什么样的？有几间卧室和卫生间？你的卧室是怎样的？",
        "Can you describe the neighborhood you grew up in?": "请描述你成长所在的社区或 neighborhood。",
        "Tell me about your parents. Where were they born? When were they born? What memories do you have of them?":
            "请谈谈你的父母：他们在哪里出生、何时出生？你对他们有哪些记忆？",
        "Who was more strict: your mother or your father? Do you have a vivid memory of something you did that you were disciplined for?":
            "小时候谁更严格——母亲还是父亲？你是否记得因某事被管教的一次鲜明经历？",
        "Did your parents have a good marriage?": "你认为父母的婚姻好吗？",
        "How did your family earn money? How did your family compare to others in the neighborhood – richer, poorer, the same?":
            "家庭如何挣钱？与社区里其他家庭相比，你们更富裕、更贫穷还是差不多？",
        "What kinds of things did your family spend money on?": "家里通常把钱花在哪些事情上？",
        "How many brothers and sisters do you have? When were they born? What memories do you have of each of them from when you were growing up?":
            "你有几个兄弟姐妹？他们何时出生？成长过程中你对各自有哪些记忆？",
        "Did you have grandparents? Where were they born? When were they born? What do you remember about them? When did they die?":
            "你有祖父母吗？他们在哪里出生、何时出生？你记得什么？他们何时去世？",
        "Did you have any pets?": "小时候养过宠物吗？",
        "What were you like as a child? What did you like to eat? What did you do for fun? What were your favorite toys or games? Did you ever have a secret place or a favorite hiding spot?":
            "小时候你是什么样的人？喜欢吃什么、玩什么？最喜欢的玩具或游戏是什么？有没有秘密基地或藏身处？",
        "What did you wear?": "小时候通常穿什么？",
        "Did you get an allowance? How much? Did you spend it right away, or save it? What did you buy?":
            "你有零花钱吗？多少？当场花掉还是存起来？买了什么？",
        "What responsibilities did you have at home when you were young?": "小时候在家有哪些责任？",
        "What kind of school did you go to? Were you a good student? What was your favorite subject? Least favorite? Who were your friends? Who was your favorite teacher and why?":
            "你上什么样的学校？成绩如何？最喜欢和最不喜欢的科目是什么？朋友是谁？最喜欢的老师是谁，为什么？",
        "Did you have any heroes or role models when you were a child?": "小时候有偶像或榜样吗？",
        "How did you spend your summer holidays? What were your favorite summer activities?":
            "暑假怎么过？最喜欢的夏日活动是什么？",
        "Where did your family go on vacations?": "家庭度假通常去哪里？",
        "How did your family celebrate holidays (e.g. Thanksgiving, Christmas, New Year, Easter, Memorial Day)? Did lots of relatives get together? What traditions did you have year after year? What food was served?":
            "家庭如何庆祝节日？亲戚会聚在一起吗？有哪些年复一年保留的传统？桌上通常有什么食物？",
        "What was the best gift you remember receiving as a child?": "小时候收到过最好的礼物是什么？",
        "What did you want to be when you grew up?": "小时候长大后想做什么？",
        "What big world events do you remember from the time you were growing up?":
            "成长过程中你记得哪些重大世界事件？",
        "What inventions do you most remember?": "你最记得哪些发明？",
        "What's different about growing up today from when you were growing up?":
            "与你成长时相比，今天的成长环境有什么不同？",
        "When you were a teenager, what did you do for fun? Did you have a favorite spot to \"hang out\"? What time did you have to be home at night? Did you ever get into any trouble?":
            "青少年时期你怎么玩？有常去的「据点」吗？晚上必须几点回家？有没有惹过麻烦？",
        "Were there any phrases that were popular when you were a teenager? What did you like to wear? How did your parents feel about the way you talked and what you wore?":
            "青少年时流行什么说法？你喜欢穿什么？父母对你说话方式和穿着怎么看？",
        "When did you learn how to drive? Who taught you? What was your first car like?":
            "你何时学会开车？谁教的？第一辆车是什么样的？",
        "What was your graduation from high school like?": "高中毕业典礼是什么样的？",
        "What dreams and goals did you have for your life when you graduated?":
            "毕业时你对人生有哪些梦想和目标？",
        "Did you go to university or college? How did you decide what you wanted to study?":
            "你上过大学吗？如何决定学什么？",
        "Did you serve in the military? What did you do and what kind of experience was it?":
            "你服过兵役吗？做什么？那是什么样的经历？",
        "How did you decide what you wanted to do with your life? How do you feel about that choice?":
            "你如何决定一生想做什么？现在如何看待这个选择？",
        "What was your first job? What did you like or not like about it?":
            "第一份工作是什么？喜欢和不喜欢的分别是什么？",
        "What job did you do most of your life? What did you like most about it? Least?":
            "一生中做得最久的工作是什么？最喜欢和最不喜欢的是什么？",
        "How did you meet your spouse? What did you like about him/her?":
            "你如何遇见配偶？喜欢他/她什么？",
        "How and when did you get engaged?": "你们何时、如何订婚？",
        "When did you get married? How old were you? Where did you get married? What was your wedding like?":
            "何时结婚？当时多大？在哪里办婚礼？婚礼是什么样的？",
        "What was the first big purchase you made with your spouse?":
            "与配偶一起的第一笔大额消费是什么？",
        "What makes your spouse special or unique?": "配偶有什么特别或独特之处？",
        "How many children do you have? When were they born? How did you decide what to name each?":
            "你有几个孩子？何时出生？如何决定名字？",
        "What's your favorite story about each of your children?": "关于每个孩子，你最喜欢的一个故事是什么？",
        "What is something funny or embarrassing one of your children said at an early age that you'll never forget?":
            "孩子小时候说过什么有趣或尴尬的话让你至今难忘？",
        "What's the most memorable family vacation you took?": "最难忘的一次家庭度假是什么？",
        "What do you remember about holiday celebrations? Is there one holiday memory that stands out for you?":
            "关于节日庆祝你记得什么？有没有特别突出的节日记忆？",
        "How did you feel about raising your children? What was the best part? The hardest part?":
            "养育孩子对你意味着什么？最好和最难的部分分别是什么？",
        "What makes you proud of your children?": "孩子的什么让你感到骄傲？",
        "How is my father/mother like me? Unlike me?": "你的父亲/母亲哪些方面像你、哪些方面不像？",
        "What do you remember about me when I was born? What about when I was younger than I am now?":
            "我出生时你记得什么？比我现在更小的时候呢？",
        "What the best thing about being a parent? A grandparent?":
            "为人父母/为人祖父母最好的一点是什么？",
        "Do you know the meaning of your family name? Are there stories about the origins of your family name?":
            "你知道姓氏的含义吗？有关于姓氏起源的故事吗？",
        "Have you ever had any nicknames as a child or as an adult? Where did they come from?":
            "童年或成年后有过绰号吗？怎么来的？",
        "How are you like your mother? Unlike her? How are you like your father? Unlike him?":
            "你在哪些方面像母亲、不像母亲？像父亲、不像父亲？",
        "What was most important to your parents?": "对你父母来说最重要的是什么？",
        "Do you feel you're like any of your grandparents? In what ways?":
            "你觉得自己像哪位祖父母？在哪些方面？",
        "How are your children like you? Unlike you?": "孩子在哪些方面像你、不像你？",
        "What do you think are your three best qualities? Your three worst?":
            "你认为自己的三个优点和三个缺点是什么？",
        "Which do you think you have the most of: talent, intelligence, education, or persistence? How has it helped you in your life?":
            "天赋、智力、教育还是坚持——你认为哪一项最多？它如何帮助了你？",
        "Do you have any special sayings or expressions?": "有什么特别的口头禅或说法吗？",
        "What's your favorite book and why? What's your favorite movie and why?":
            "最喜欢的书/电影是什么？为什么？",
        "Who are three people in history you admire most and why?":
            "历史上最敬佩的三个人是谁？为什么？",
        "What have been the three biggest news events during your lifetime and why?":
            "一生中三件最大的新闻事件是什么？为什么？",
        "If you could travel into the future, would you rather see something that specifically relates to you, or something that relates to the future of the country in general? Why?":
            "若能去未来，你更想看与自己相关的事还是国家整体的事？为什么？",
        "If you could have three wishes, what would they be?": "若有三个愿望，会是什么？",
        "If you won $1 million tomorrow, what would you do with the money?":
            "若明天赢得一百万，你会怎么花？",
        "What's the highest honor or award you've ever received?": "你获得过的最高荣誉或奖项是什么？",
        "What's the most memorable phone call you've ever received?": "接到过最难忘的一通电话是什么？",
        "What's the best compliment you ever received?": "收到过最好的赞美是什么？",
        "What kinds of things bring you the most pleasure now? When you were a younger adult? A child?":
            "现在、年轻时、童年时，分别什么事带给你最大快乐？",
        "What things frighten you now? What frightened you when you were a younger adult? A child?":
            "现在、年轻时、童年时，分别什么让你害怕？",
        "What's the one thing you've always wanted but still don't have?":
            "一直想要但至今没有的东西是什么？",
        "Do you feel differently about yourself now from how you felt when you were younger? How?":
            "你现在对自己的感受与年轻时不同吗？如何不同？",
        "What do you think has stayed the same about you throughout life? What do you think has changed?":
            "一生中哪些方面始终如一？哪些方面改变了？",
        "Do you have any hobbies or special interests? Do you enjoy any particular sports?":
            "有什么爱好或特别兴趣吗？喜欢什么运动吗？",
        "What's your typical day like now? How is it different from your daily routines in the past?":
            "现在典型的一天是怎样的？与过去日常有何不同？",
        "Is the present better or worse than when you were younger?": "现在比年轻时更好还是更糟？",
        "What do you do for fun?": "你现在做什么来娱乐？",
        "Who do you trust and depend on?": "你信任并依赖谁？",
        "What things are most important to you now? Why?": "现在对你最重要的是什么？为什么？",
        "How have your dreams and goals changed through your life?":
            "人生中的梦想和目标如何变化？",
        "What do you remember about your 20s? 30s? 40s? 50s? 60s? What events stand out in your mind? How was each age different from the one before it?":
            "你对 20、30、40、50、60 岁各有什么记忆？哪些事件突出？每个年龄段与上一段有何不同？",
        "There are some ages we don't look forward to. What birthday were you least enthusiastic about? Why?":
            "有没有不太想面对的年龄？哪个生日最让你提不起劲？为什么？",
        "If you could go back to any age, which age would it be and why?":
            "若能回到某个年龄，会是几岁？为什么？",
        "How do you feel now about growing old? What's the hardest thing about growing older? The best thing?":
            "现在如何看待变老？最难和最好的是什么？",
        "What were your parents like when they got older?": "父母年老时是什么样的？",
        "Did you have any expectations at points in your life about what growing older would be like for you?":
            "人生中是否曾对变老有过预期？",
        "How should a person prepare for old age? Is there anything you wish you'd done differently?":
            "人应如何准备老年？有什么希望做得不同的事吗？",
        "Do you think about the future and make plans? What are your concerns for the future?":
            "你会思考未来并做计划吗？对未来的担忧是什么？",
        "If you live another 20-30 years, what will you do? Do you want to live another 20-30 years?":
            "若再活二三十年，你会做什么？你想再活那么久吗？",
        "What do you look forward to now?": "现在最期待什么？",
        "What's your most cherished family tradition? Why is it important?":
            "最珍视的家庭传统是什么？为什么重要？",
        "What have you liked best about your life so far? What's your happiest or proudest moment?":
            "到目前为止最喜欢的人生部分是什么？最快乐或最骄傲的时刻？",
        "What do you feel have been the important successes in your life? The frustrations?":
            "人生中重要的成功和挫折分别是什么？",
        "What's the most difficult thing that ever happened to you? How did you deal with it?":
            "发生在你身上最难的事是什么？如何应对？",
        "What do you think the turning points have been in your life? What were you like then?":
            "人生中的转折点有哪些？当时你是什么样的人？",
        "Are there times of your life that you remember more vividly than others? Why?":
            "有没有记得特别清晰的时期？为什么？",
        "What have been the most influential experiences in your life?":
            "对你影响最大的经历是什么？",
        "Describe a person or situation from your childhood that had a profound effect on the way you look at life.":
            "描述童年中一个人或情境，它深刻影响了你看世界的方式。",
        "If you were writing the story of your life, how would you divide it into chapters?":
            "若把人生写成书，你会如何分章节？",
        "What, if anything, would you have done differently in your life?":
            "若有重来机会，你会改变什么？",
        "What do you know now that you wish you'd known when you were young?":
            "现在知道而希望年轻时就知道的事是什么？",
        "What have you thrown away in your life that you wish you hadn't? What have you held on to that's important and why is it important? What \"junk\" have you held on to and why?":
            "扔掉了什么后来后悔？保留了什么重要的东西？又保留了什么「无用之物」？",
        "Over time, how have you changed the way you look at life/people?":
            "随着时间，你看待生活/他人的方式如何改变？",
        "What advice did your grandparents or parents give you that you remember best?":
            "祖父母或父母给过而记得最牢的建议是什么？",
        "Do you have a philosophy of life? What's your best piece of advice for living? If a young person came to you asking what's the most important thing for living a good life, what would you say?":
            "有人生哲学吗？最好的生活建议是什么？若年轻人问如何过好一生，你会说什么？",
        "How do you define a \"good life\" or a \"successful life\"?":
            "你如何定义「好人生」或「成功人生」？",
        "Do you think a person needs to first overcome serious setbacks or challenges to be truly successful?":
            "你认为人是否必须先克服重大挫折才算真正成功？",
        "In what way is it important to know your limitations in your life or career?":
            "认识自身局限在人生或职业中为何重要？",
        "If you had the power to solve one and only one problem in the world, what would it be and why?":
            "若只能解决世界一个问题，会是什么？为什么？",
        "What do you see as your place or purpose in life? How did you come to that conclusion?":
            "你认为自己在人生中的位置或目的是什么？如何得出这个结论？",
        "What would you like your children and grandchildren to remember about you?":
            "希望子女和孙辈记住你什么？",
        "If you could write a message to each of your children and grandchildren and put it in a time capsule for them to read 20 years from now, what would you write to each?":
            "若给每个孩子/孙辈写一封二十年后打开的时间胶囊信，你会写什么？",
    }
    en = en.strip().replace("\n", " ").replace("  ", " ")
    en = en.replace("'", "'").replace(""", '"').replace(""", '"')
    if en in mapping:
        return mapping[en]
    if "my father/mother" in en.lower():
        return "你的父亲/母亲哪些方面像你、哪些方面不像？"
    return en  # fallback


def extract_lifeintquestions() -> tuple[list[dict], list[dict]]:
    text = (LIB / "12-lifeintquestions-生命访谈问题.pdf").read_text(encoding="utf-8", errors="replace")
    skip = re.compile(
        r"^(Life Interview|Life Events|Identity|The Present|Aging|© SV Bosak|-- \d|Life Lessons)",
        re.I,
    )
    body = []
    for line in text.splitlines():
        s = line.strip()
        if not s or skip.match(s):
            continue
        body.append(s)
    blob = " ".join(body)
    parts = re.split(r"\?\s*", blob)
    chunks = [p.strip() + "?" for p in parts if len(p.strip()) > 12]

    records: list[dict] = []
    rejected: list[dict] = []
    seen: set[str] = set()

    for chunk in chunks:
        if len(chunk) < 15 or chunk.startswith("©"):
            continue
        if "Hold a mirror" in chunk:
            rejected.append(
                {
                    "question": chunk,
                    "reason": "intimate_dyadic",
                    "note": "访谈者动作 Hold a mirror；已跳过",
                }
            )
            continue
        if "my father/mother like me" in chunk.lower():
            rejected.append(
                {
                    "question": chunk,
                    "reason": "intimate_dyadic",
                    "note": "my father/mother like me 二元指称；跳过",
                }
            )
            continue
        if "about me when I was born" in chunk.lower():
            chunk = chunk.replace("about me when I was born", "when you were born")
            chunk = chunk.replace("when I was younger than I am now", "from your early years")
        zh = _life_q(chunk)
        if zh == chunk and not re.search(r"[\u4e00-\u9fff]", zh):
            status = "candidate"
        else:
            status = "active"
        if zh in seen:
            continue
        seen.add(zh)
        low = chunk.lower()
        if any(w in low for w in ("marriage", "spouse", "children", "parent", "grandparent")):
            if "children" in low and "how many" in low:
                cat, sub, pre = "real", "为人父母", ["has_children"]
            elif "spouse" in low or "married" in low or "engaged" in low:
                cat, sub, pre = "emo", "爱情与婚姻", ["has_been_married"]
            elif "grandparent" in low:
                cat, sub, pre = "real", "家族传承", ["has_grandparents_met"]
            else:
                cat, sub, pre = "real", "家庭与成长", None
        elif any(w in low for w in ("job", "military", "university", "career")):
            cat, sub, pre = "real", "职业与经历", ["has_work_experience"] if "first job" in low or "most of your life" in low else None
        elif any(w in low for w in ("philosophy", "advice", "successful", "purpose", "wishes")):
            cat, sub, pre = "val", "人生教训", None
        elif any(w in low for w in ("afraid", "frighten", "pleasure", "feel differently")):
            cat, sub, pre = "emo", "情绪体验", None
        elif any(w in low for w in ("growing old", "future", "20-30 years", "prepare for old")):
            cat, sub, pre = "val", "人生目标", None
        else:
            cat, sub, pre = "real", "家庭与成长", None
        rec: dict[str, str | list[str]] = {
            "question": zh,
            "category": cat,
            "subcategory": sub,
            "type": "open",
            "interaction": "story" if cat == "real" else "reflection",
            "source": "lifeintquestions",
            "status": status,
        }
        if pre:
            rec["prerequisites"] = pre
        records.append(rec)
    return records, rejected


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main() -> int:
    whoqol = extract_whoqol()
    mbti = extract_mbti()
    mmdi = extract_mmdi()
    life, life_rej = extract_lifeintquestions()

    write_jsonl(PENDING / f"WHOQOL-{DATE}.jsonl", whoqol)
    write_jsonl(PENDING / f"MBTI-{DATE}.jsonl", mbti)
    write_jsonl(PENDING / f"MMDI-{DATE}.jsonl", mmdi)
    write_jsonl(PENDING / f"lifeintquestions-{DATE}.jsonl", life)
    if life_rej:
        write_jsonl(PENDING / f"lifeintquestions-{DATE}.rejected.jsonl", life_rej)

    print(f"WHOQOL: {len(whoqol)}")
    print(f"MBTI: {len(mbti)}")
    print(f"MMDI: {len(mmdi)}")
    print(f"lifeintquestions: {len(life)} (rejected sidecar: {len(life_rej)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
