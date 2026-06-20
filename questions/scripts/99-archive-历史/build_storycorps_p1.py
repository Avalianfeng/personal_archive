#!/usr/bin/env python3
"""One-shot: merge StoryCorps P1 questions from good question.md into 02-问题地图-Views/*.md."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = ROOT / "categories"

PREFIX = {
    "real": "REAL",
    "emo": "EMO",
    "dec": "DEC",
    "sta": "STA",
    "self": "SELF",
    "val": "VAL",
    "oth": "OTH",
}

FILE_NAMES = {
    "real": "现实问题.md",
    "emo": "情感问题.md",
    "dec": "决策问题.md",
    "sta": "状态问题.md",
    "self": "自我认知.md",
    "val": "价值问题.md",
    "oth": "其他.md",
}

# (category, subcategory, interaction, text, tags?, skip_key?)
# skip_key: normalized text for exact-duplicate detection within batch
QUESTIONS: list[tuple] = [
    # === Great Questions for Anyone ===
    ("real", "家庭与成长", "story", "你能跟我说说你生命中重要的人吗？", ["family"]),
    ("real", "时间线与事件", "story", "你人生中最快乐的时刻是什么？最悲伤的时刻又是什么？"),
    ("real", "时间线与事件", "story", "谁对你的人生影响最大？这个人或这些人教会了你什么？"),
    ("real", "时间线与事件", "story", "你能跟我说说生活中某个人的善意如何改变了你的人生吗？"),
    ("val", "人生教训", "reflection", "你在人生中学到的最重要的一课是什么？"),
    ("real", "家庭与成长", "story", "你最早的记忆是什么？", ["childhood"]),
    ("emo", "亲密关系", "story", "你最喜欢我的哪段回忆？"),
    ("real", "家庭与成长", "story", "你有没有什么关于你的趣事，家人经常讲？", ["family"]),
    ("real", "家庭与成长", "story", "你生活中有什么有趣的故事、回忆或人物想跟我分享吗？"),
    ("self", "自我欣赏与不足", "reflection", "你最引以为豪的是什么？"),
    ("emo", "孤独与依恋", "story", "你一生中什么时候感到最孤独？"),
    ("emo", "情绪表达", "story", "如果可以永远保留人生中的某些记忆，你会选择哪些？"),
    ("self", "自我描述", "reflection", "你的生活与你想象中的有何不同？"),
    ("val", "人生目标", "future", "你希望人们如何记住你？", None, "remembered"),
    ("self", "自我欣赏与不足", "reflection", "你后悔过吗？"),
    ("val", "人生目标", "future", "你的未来会怎样？"),
    ("emo", "亲密关系", "future", "你对我的未来有什么期望？"),
    ("emo", "亲密关系", "future", "你对我的孩子们有什么期望？"),
    ("emo", "亲密关系", "story", "如果这是我们最后一次谈话，你有什么想对我说的吗？"),
    ("val", "人生教训", "future", "对于多年以后聆听这段话的子孙后代，你有什么智慧想要传承给他们？你希望他们知道些什么？"),
    ("emo", "亲密关系", "story", "有没有什么你一直想告诉我但现在还没告诉我的事？"),
    ("emo", "亲密关系", "reflection", "关于我，你有没有一些一直想知道但从未问过的事情？"),
    ("self", "自我描述", "reflection", "如果你能和年轻时的自己对话，你会说什么？"),
    ("emo", "亲密关系", "story", "你对我的第一印象是什么？后来又发生了怎样的变化？"),
    # === Friends and Colleagues ===
    ("oth", "对话引导", "reflection", "如果你可以采访生活中任何一位在世或已故的人，但不能是名人，你会选择谁？为什么？"),
    ("emo", "友谊", "story", "你对我的第一个记忆是什么？"),
    ("emo", "友谊", "story", "你有没有不喜欢过我的时候？"),
    ("emo", "友谊", "reflection", "是什么让我们成为如此好的朋友？"),
    ("self", "他人评价", "reflection", "你会如何形容我？你会如何形容你自己？"),
    ("emo", "友谊", "future", "10年后、20年后，我们会身处何方？"),
    ("emo", "友谊", "future", "你觉得我们会失去联系吗？"),
    # === Grandparents ===
    ("real", "家庭与成长", "story", "你在哪里长大？", ["childhood"], "grow_up"),
    ("real", "家庭与成长", "story", "你的童年是怎样的？", ["childhood"]),
    ("real", "家庭与成长", "story", "你最喜欢的亲戚是谁？", ["family"], "favorite_relatives"),
    ("real", "家庭与成长", "story", "你还记得祖父母曾经给你讲过的故事吗？", ["family", "childhood"]),
    ("real", "家庭与成长", "story", "你和爷爷奶奶是怎么认识的？"),
    ("real", "家庭与成长", "story", "我小时候，我的妈妈/爸爸/父母是什么样的？"),
    ("real", "家庭与成长", "story", "你的祖父母举止得体吗？"),
    ("real", "家庭与成长", "story", "你祖父母做过的最糟糕的事是什么？"),
    ("real", "家庭与成长", "story", "你的父母是什么样的人？", ["family"], "parents_like"),
    ("real", "家庭与成长", "story", "你的祖父母是什么样的人？", ["family"]),
    ("emo", "亲密关系", "reflection", "你以我为荣吗？"),
    # === Raising Children ===
    ("real", "家庭与成长", "story", "你是什么时候得知自己即将为人父母的？当时你是什么感受？", ["family"]),
    ("real", "家庭与成长", "reflection", "你一直都知道自己想当父母吗？"),
    ("real", "家庭与成长", "story", "你能描述一下你第一次见到孩子的那一刻吗？", ["family"]),
    ("self", "角色认同", "reflection", "为人父母后，你发生了哪些变化？"),
    ("self", "自我描述", "reflection", "为人父母后，你对自己有了哪些新的认识？"),
    ("emo", "亲密关系", "future", "你对你的孩子有什么期望？"),
    ("real", "家庭与成长", "story", "你还记得你最后一个孩子永远离开家是什么时候吗？", ["family"]),
    ("real", "家庭与成长", "story", "你有没有关于孩子的特别喜欢的故事？", ["family"]),
    # === Parents ===
    ("real", "家庭与成长", "story", "你还记得第一次见到我时，你脑子里在想什么吗？", ["family"]),
    ("real", "家庭与成长", "story", "你是怎么给我取这个名字的？", ["family"]),
    ("real", "家庭与成长", "story", "我小时候是什么样的？婴儿时期是什么样的？幼儿时期又是什么样的？", ["childhood"]),
    ("real", "家庭与成长", "story", "我的兄弟姐妹是什么样的人？", ["family"]),
    ("emo", "亲密关系", "story", "在我成长过程中，你经历过的最艰难的时刻是什么？"),
    ("dec", "假设与取舍", "scenario", "如果一切可以重来，你会用不同的方式养育我吗？"),
    ("val", "人生教训", "reflection", "关于如何养育自己的孩子，您有什么建议？"),
    ("emo", "亲密关系", "future", "你对我有什么期望？"),
    ("real", "家庭与成长", "story", "你是怎么认识你妈妈/爸爸的？"),
    ("self", "角色认同", "reflection", "你觉得我们有哪些相似之处？你觉得我们有哪些不同之处？"),
    # === Growing Up ===
    ("real", "家庭与成长", "story", "你何时何地出生？", ["childhood"]),
    ("real", "家庭与成长", "story", "在那里成长是什么样的？", ["childhood"]),
    ("real", "家庭与成长", "story", "你的父母是谁？", ["family"]),
    ("real", "家庭与成长", "story", "你和父母的关系如何？", ["family"]),
    ("real", "家庭与成长", "story", "你惹过麻烦吗？你做过的最糟糕的事是什么？", ["childhood"]),
    ("real", "家庭与成长", "story", "你有兄弟姐妹吗？他们小时候是什么样的？", ["family", "childhood"]),
    ("real", "家庭与成长", "story", "你当时的长相如何？", ["childhood"]),
    ("self", "自我描述", "story", "你如何描述自己的童年？你快乐吗？", ["childhood"]),
    ("real", "家庭与成长", "story", "你童年时期最美好的回忆是什么？最糟糕的回忆又是什么？", ["childhood"]),
    ("real", "家庭与成长", "story", "你有昵称吗？是怎么来的？", ["childhood"]),
    ("real", "家庭与成长", "story", "你最好的朋友是谁？他们是什么样的人？", ["childhood", "friendship"]),
    ("real", "家庭与成长", "story", "你年轻的时候，会如何描述你理想中的完美一天？", ["childhood"]),
    ("real", "家庭与成长", "story", "你想象中长大后的生活会是什么样子？", ["childhood"]),
    ("real", "家庭与成长", "story", "你童年时期有没有什么特别喜欢的故事？", ["childhood"]),
    ("real", "教育与求学", "story", "小时候，你长大后想成为什么样的人？", ["childhood"]),
    # === School ===
    ("real", "教育与求学", "story", "你喜欢上学吗？"),
    ("real", "教育与求学", "story", "你以前是哪种类型的学生？"),
    ("real", "教育与求学", "story", "你那时做什么来消遣？"),
    ("self", "他人评价", "reflection", "你的同学会如何记住你？"),
    ("emo", "友谊", "story", "你现在还和那时认识的人保持联系吗？"),
    ("real", "教育与求学", "story", "你学生时代最美好的回忆是什么？最糟糕的回忆又是什么？"),
    ("real", "教育与求学", "story", "有没有哪位老师对你的人生产生了特别大的影响？请跟我讲讲他们。", None, "teacher_influence"),
    ("real", "教育与求学", "story", "你有没有在学校时期特别喜欢的故事？"),
    # === Teachers ===
    ("real", "职业与经历", "story", "你是什么时候、为什么决定当一名教师的？"),
    ("real", "职业与经历", "story", "请跟我讲讲你当教师的第一天。"),
    ("real", "职业与经历", "reflection", "实际的教学与你想像中有何不同？"),
    ("emo", "情绪表达", "story", "有没有哪次教学经历让你感到充满希望？"),
    ("real", "职业与经历", "story", "你在课堂上经历过的最具挑战或最有趣的时刻是什么？"),
    ("val", "人生目标", "reflection", "你希望学生如何记住你？"),
    ("real", "教育与求学", "story", "有没有哪位老师对你的人生产生了特别大的影响？你从他们身上学到了什么关于教学的事？", None, "teacher_influence2"),
    ("val", "人生教训", "reflection", "回顾过去，你会给刚入职第一年的自己什么建议？"),
    # === Love & Relationships ===
    ("emo", "爱情与婚姻", "story", "你这辈子有没有真正爱过的人？"),
    ("emo", "爱情与婚姻", "story", "你第一次坠入爱河是什么时候？"),
    ("emo", "爱情与婚姻", "story", "你能跟我讲讲你的初吻吗？"),
    ("emo", "爱情与婚姻", "story", "你的第一段认真恋情是什么样的？"),
    ("emo", "爱情与婚姻", "reflection", "你相信一见钟情吗？"),
    ("emo", "爱情与婚姻", "story", "你会想起以前的恋人吗？"),
    ("emo", "爱情与婚姻", "reflection", "你从过往的感情关系中学到了什么？"),
    ("emo", "爱情与婚姻", "story", "你生命中有没有「错过的人」？"),
    ("emo", "爱情与婚姻", "story", "你经历过的最痛苦的分手是什么样的？"),
    ("emo", "爱情与婚姻", "story", "你还记得你经历过的最棒的一次约会吗？/你还记得你的第一次约会吗？"),
    # === Marriage & Partnerships ===
    ("real", "家庭与成长", "story", "你是怎么认识你的配偶/伴侣的？"),
    ("emo", "爱情与婚姻", "story", "你怎么知道对方就是「那个人」？"),
    ("real", "家庭与成长", "story", "你是怎么求婚的？"),
    ("emo", "爱情与婚姻", "story", "婚姻中最美好的时光是什么？最艰难的时期又是什么？"),
    ("dec", "假设与取舍", "scenario", "你有没有想过离婚？"),
    ("real", "家庭与成长", "story", "你有没有离过婚？能跟我讲讲吗？"),
    ("val", "人生教训", "reflection", "你对年轻情侣有什么建议？"),
    ("real", "家庭与成长", "story", "你有没有关于婚姻或伴侣的特别喜欢的故事？"),
    # === Working ===
    ("real", "职业与经历", "story", "请描述一下你所做的工作。"),
    ("real", "职业与经历", "story", "你是怎么进入这一行的？"),
    ("sta", "动力与方向", "self_report", "你喜欢你的工作吗？"),
    ("real", "职业与经历", "story", "你的工作经历教会了你什么？"),
    ("dec", "假设与取舍", "scenario", "如果现在可以做任何事，你会做什么？为什么？"),
    ("real", "职业与经历", "future", "你打算退休吗？如果打算，什么时候？你对此有什么感受？"),
    ("real", "职业与经历", "story", "你有没有关于工作经历特别喜欢的故事？"),
    # === Religion ===
    ("val", "信仰与信念", "story", "能跟我讲讲你的宗教信仰或精神信仰吗？你的宗教是什么？"),
    ("val", "信仰与信念", "story", "你是如何走上信仰之路的？来自家庭，还是某段或某些经历？"),
    ("val", "信仰与信念", "reflection", "你的信仰随时间发生了怎样的变化？"),
    ("val", "信仰与信念", "story", "你有没有经历过奇迹？"),
    ("val", "信仰与信念", "story", "你人生中最深刻的灵性时刻是什么？"),
    ("val", "信仰与信念", "reflection", "你相信上帝吗？"),
    ("val", "信仰与信念", "story", "你在人生中如何体验过上帝（或更高的力量）？"),
    ("val", "信仰与信念", "reflection", "你相信来世吗？你认为那会是什么样子？", None, "afterlife"),
    ("val", "信仰与信念", "reflection", "当你见到上帝时，你想说什么？"),
    ("val", "信仰与信念", "story", "有没有考验过你信仰的时刻？那些挑战是什么，对你的信仰产生了什么影响？"),
    # === Serious Illness ===
    ("real", "疾病经历", "story", "能跟我讲讲你的病情吗？"),
    ("sta", "疾病与身心", "self_report", "你会想到死亡吗？你害怕吗？"),
    ("sta", "疾病与身心", "reflection", "你如何想像自己的死亡？"),
    ("val", "信仰与信念", "reflection", "你相信来世吗？", None, "afterlife2"),
    ("self", "自我欣赏与不足", "reflection", "你有什么遗憾吗？"),
    ("self", "自我描述", "reflection", "确诊之后，你看待生活的方式与之前有什么不同了吗？"),
    ("val", "人生目标", "future", "你有什么遗愿吗？"),
    ("val", "人生教训", "reflection", "如果想给我或家里其他人建议，你会说什么？"),
    ("val", "人生教训", "reflection", "你从生活中学到了什么？最重要的是哪些？"),
    ("self", "自我描述", "reflection", "这场病改变你了吗？你学到了什么？"),
    # === Family Heritage ===
    ("real", "家族传承", "story", "你父母的家族来自哪里？"),
    ("real", "家族传承", "story", "你去过那里吗？那是什么体验？"),
    ("real", "家族传承", "story", "你们家有哪些代代相传的传统？"),
    ("real", "家族传承", "story", "你还记得他们以前给你讲过的故事吗？"),
    ("real", "家族传承", "story", "经典的家庭故事有哪些？"),
    # === Military (subset with unique content; many similar grouped) ===
    ("real", "军旅经历", "story", "你是什么时候被征召入伍的？还是什么时候入伍的？"),
    ("real", "军旅经历", "story", "你还记得入伍那天的情况吗？"),
    ("real", "军旅经历", "story", "你是如何告诉家人和朋友你要参军的？那段时间里有哪些对话让你印象特别深刻？"),
    ("real", "军旅经历", "story", "如果你应征入伍，你加入军队的原因有哪些？你是如何选择你的兵种的？"),
    ("real", "军旅经历", "reflection", "入伍前你对军旅生活有怎样的想象？服役后你的看法发生了哪些变化？"),
    ("real", "军旅经历", "story", "新兵训练是什么样的？"),
    ("real", "军旅经历", "story", "你能描述一下你在军队服役期间发生的一件趣事吗？"),
    ("real", "军旅经历", "story", "你还记得适应军旅生活的一些事情吗？"),
    ("real", "军旅经历", "story", "战争期间你在哪里服役？"),
    ("real", "军旅经历", "story", "如果你被派往海外服役，你是如何告诉你的亲人的？"),
    ("real", "军旅经历", "story", "你是如何与家乡的亲朋好友保持联系的？"),
    ("real", "军旅经历", "story", "你对那次部署印象最深刻的是什么？"),
    ("real", "军旅经历", "story", "如果你参与过多次部署，它们之间有何不同？你是如何调整的？"),
    ("emo", "情绪表达", "story", "你能描述一下你从战场归来时的感受吗？"),
    ("emo", "情绪表达", "story", "你有没有特别怀念平民生活的什么？"),
    ("real", "军旅经历", "story", "你服役期间有没有哪位同事让你印象特别深刻？你能跟我说说他/她吗？"),
    ("real", "军旅经历", "story", "在服役期间，你和朋友们一起做过哪些有趣的事情？"),
    ("real", "军旅经历", "story", "你的军人朋友之间有没有互相恶作剧？你能描述一个好笑的例子吗？"),
    ("real", "军旅经历", "story", "你有没有因为违反规则而被抓到过？你有没有做过不该做的事却侥幸逃脱过惩罚？"),
    ("real", "军旅经历", "story", "你有没有了解到过一些关于战友的让你感到惊讶的事情？"),
    ("real", "军旅经历", "story", "你何时退伍的？退伍过程是怎样的？"),
    ("real", "军旅经历", "story", "你退伍后的头几个月过得怎么样？"),
    ("real", "军旅经历", "story", "从军人过渡到平民生活的过程中，有没有什么人或事帮助你？"),
    ("val", "人生教训", "reflection", "对于即将退役的军人，您有什么建议？"),
    ("self", "自我描述", "reflection", "你认为你的军旅生涯对你有什么影响？"),
    ("self", "自我描述", "reflection", "军旅生涯中，你对自己有了哪些新的认识？"),
    ("val", "人生目标", "future", "你对未来有哪些期望？"),
    ("real", "军旅经历", "reflection", "服役之后，有哪些词语或短语对你来说再也不一样了？"),
    ("emo", "情绪表达", "story", "你刚退伍的时候，有哪些平民的方面让你难以接受？"),
    ("val", "人生教训", "reflection", "你希望平民百姓对兵役有哪些了解？"),
    ("real", "军旅经历", "reflection", "在部队里，你养成了哪些喜欢的习惯？又有哪些不喜欢的？"),
    ("emo", "情绪表达", "story", "你怀念军旅生涯中的哪些方面？又有哪些方面让你庆幸已经告别？"),
    ("emo", "亲密关系", "story", "在与家人和朋友谈论你的军旅生涯时，有哪些难以沟通的地方？"),
    ("val", "人生教训", "reflection", "您对其他军人夫妇有什么建议吗？"),
    ("real", "军旅经历", "story", "如果你有孩子，你想让他们了解你服兵役的哪些方面？"),
    # === Remembering the Fallen (templates) ===
    ("oth", "缅怀模板", "story", "缅怀逝者：你与_______是什么关系？"),
    ("oth", "缅怀模板", "story", "缅怀逝者：请告诉我关于_______的故事。"),
    ("oth", "缅怀模板", "story", "缅怀逝者：_______长什么样？"),
    ("oth", "缅怀模板", "story", "缅怀逝者：你最难忘的关于_______的回忆是什么？"),
    ("oth", "缅怀模板", "story", "缅怀逝者：你是如何得知_______去世的消息的？"),
    ("emo", "哀伤与失去", "story", "缅怀逝者：在悲痛中，什么对你帮助最大？", None, "grief_help"),
    ("oth", "缅怀模板", "story", "缅怀逝者：你们有什么传统来纪念_______？"),
    ("oth", "缅怀模板", "story", "缅怀逝者：你们俩之间有没有什么趣事可以分享？"),
    # === Remembering a Loved One ===
    ("oth", "缅怀模板", "story", "你和_____是什么关系？"),
    ("oth", "缅怀模板", "story", "请告诉我关于_____的事情。"),
    ("emo", "哀伤与失去", "story", "你对_____的第一个记忆是什么？"),
    ("emo", "哀伤与失去", "story", "你对_____最美好的回忆是什么？"),
    ("emo", "哀伤与失去", "story", "你对_____印象最深刻的记忆是什么？"),
    ("emo", "哀伤与失去", "story", "对你来说，_____意味着什么？"),
    ("emo", "哀伤与失去", "story", "你愿意/可以谈谈_____的死吗？_____是怎么死的？"),
    ("emo", "哀伤与失去", "story", "失去_____最难的是什么？"),
    ("emo", "哀伤与失去", "future", "如果_____今天在这里，你会问_____什么问题？"),
    ("emo", "哀伤与失去", "story", "你最怀念_____的什么？"),
    ("val", "人生目标", "reflection", "你认为_____希望人们如何记住他？", None, "remembered_loved"),
    ("real", "缅怀逝者", "story", "你能谈谈_____在人生中克服的最大障碍吗？"),
    ("emo", "哀伤与失去", "story", "你和_____之间有没有发生过什么分歧、争吵或冲突？"),
    ("emo", "哀伤与失去", "story", "关于_____，什么事情会让你微笑？"),
    ("emo", "亲密关系", "story", "你们的关系如何？"),
    ("real", "缅怀逝者", "story", "_____长什么样？"),
    ("emo", "哀伤与失去", "story", "你有没有特别喜欢_____以前讲的笑话？"),
    ("real", "缅怀逝者", "story", "你有什么关于_____的故事想分享吗？"),
    ("val", "人生目标", "future", "_____对未来有怎样的希望和梦想？"),
    ("oth", "缅怀模板", "story", "关于_____，你有什么觉得别人不知道的事情吗？"),
    ("self", "自我描述", "reflection", "你现在和失去_____之前相比有什么不同？"),
    ("emo", "哀伤与失去", "story", "留下最深刻印象的_____形象是什么？"),
    ("oth", "缅怀模板", "story", "你们有什么传统来纪念_____吗？"),
    ("emo", "哀伤与失去", "story", "在悲痛之中，什么对你的帮助最大？", None, "grief_help2"),
    ("emo", "哀伤与失去", "story", "最艰难的时期是什么时候？"),
    # === Justice ===
    ("real", "司法经历", "story", "请告诉我你第一次意识到刑事司法系统存在是什么时候。"),
    ("val", "底线与原则", "reflection", "你与司法系统打交道的经历是否改变了你或你的看法？如何改变的？"),
    ("real", "司法经历", "story", "刑事司法系统对你的生活产生了哪些影响？"),
    ("val", "底线与原则", "reflection", "你希望其他人了解刑事司法系统的哪些方面？"),
    ("real", "司法经历", "story", "你能描述一下你被捕的过程吗？"),
    ("real", "司法经历", "story", "你的家人和朋友是怎么知道你要坐牢的？"),
    ("real", "司法经历", "story", "监狱是什么样的？你能描述一下它的样子、气味和声音吗？"),
    ("real", "司法经历", "story", "你是如何与外界沟通的？"),
    ("emo", "情绪表达", "story", "你还记得被判有罪时的感受吗？这件事对你产生了怎样的影响？"),
    ("real", "司法经历", "story", "请告诉我你获释那天的情况。"),
    ("val", "人生教训", "reflection", "你希望有人当初告诉你哪些关于重返社会的事情？"),
    ("real", "时间线与事件", "story", "获释后你最快乐的时刻是什么？"),
    ("sta", "近期状态", "self_report", "你感到自由吗？为什么？"),
    ("val", "人生教训", "reflection", "告诉我是什么帮助你坚持下去的？"),
    ("dec", "假设与取舍", "scenario", "如果你可以改变刑事司法系统中的一件事，那会是什么？"),
]

RELATED_GROUPS: dict[str, list[str]] = {
    "remembered": ["remembered_loved"],
    "grow_up": [],
    "favorite_relatives": [],
    "parents_like": [],
    "teacher_influence": ["teacher_influence2"],
    "teacher_influence2": ["teacher_influence"],
    "afterlife": ["afterlife2"],
    "afterlife2": ["afterlife"],
    "grief_help": ["grief_help2"],
    "grief_help2": ["grief_help"],
    "remembered_loved": ["remembered"],
}

SKIP_KEYS = {
    # exact duplicate Chinese in source — second occurrence skipped
    "remembered",  # grandparents duplicate — only first kept
}

# Keys we skip on second+ occurrence (by skip_key field)
seen_skip_keys: set[str] = set()
skipped: list[str] = []


def format_block(
    qid: str,
    cat: str,
    subcategory: str,
    interaction: str,
    text: str,
    tags: list[str] | None,
    related: list[str] | None,
) -> str:
    lines = [
        f"## {subcategory}",
        "",
        "---",
        f"id: {qid}",
        f"category: {cat}",
        f"subcategory: {subcategory}",
        "type: open",
        f"interaction: {interaction}",
        "source: StoryCorps",
    ]
    if tags:
        lines.append("tags:")
        for t in tags:
            lines.append(f"  - {t}")
    lines.append("status: active")
    if related:
        lines.append("related:")
        for r in related:
            lines.append(f"  - {r}")
    lines.extend(["---", "", text, ""])
    return "\n".join(lines)


def main() -> None:
    global seen_skip_keys, skipped

    by_cat: dict[str, list[str]] = {c: [] for c in PREFIX}
    counters: dict[str, int] = {c: 0 for c in PREFIX}
    key_to_id: dict[str, str] = {}

    # self starts at 002 (Q-SELF-001 exists)
    counters["self"] = 1

    for item in QUESTIONS:
        cat, sub, interaction, text = item[0], item[1], item[2], item[3]
        tags = item[4] if len(item) > 4 and isinstance(item[4], list) else None
        skip_key = item[5] if len(item) > 5 else None

        norm = re.sub(r"\s+", "", text)
        dedup = skip_key or norm

        if skip_key and skip_key in seen_skip_keys:
            skipped.append(f"[完全重复跳过] {text[:40]}… (key={skip_key})")
            continue
        if skip_key:
            seen_skip_keys.add(skip_key)

        counters[cat] += 1
        num = counters[cat]
        qid = f"Q-{PREFIX[cat]}-{num:03d}"
        if skip_key:
            key_to_id[skip_key] = qid

        related_ids: list[str] = []
        if skip_key and skip_key in RELATED_GROUPS:
            for rk in RELATED_GROUPS[skip_key]:
                if rk in key_to_id:
                    related_ids.append(key_to_id[rk])

        by_cat[cat].append(
            format_block(qid, cat, sub, interaction, text, tags, related_ids or None)
        )

    # second pass: add related for groups where second was added after first
    # (teacher_influence2, afterlife2, grief_help2, remembered_loved)
    # Already handled at insert time for forward refs; patch backward refs in files
    content_map: dict[str, str] = {}
    for cat, blocks in by_cat.items():
        content_map[cat] = "\n".join(blocks)

    # Patch related on first items when second was processed later
    patches = [
        ("teacher_influence", "teacher_influence2"),
        ("afterlife", "afterlife2"),
        ("grief_help", "grief_help2"),
        ("remembered", "remembered_loved"),
    ]
    for a, b in patches:
        if a in key_to_id and b in key_to_id:
            aid, bid = key_to_id[a], key_to_id[b]
            for cat in PREFIX:
                if f"id: {aid}" in content_map.get(cat, ""):
                    old = f"id: {aid}\ncategory:"
                    if f"related:" not in content_map[cat].split(aid)[1].split("---")[0]:
                        content_map[cat] = content_map[cat].replace(
                            f"id: {aid}\n",
                            f"id: {aid}\n",
                            1,
                        )
                    # inject related after status: active for aid block
                    block_pat = re.compile(
                        rf"(id: {re.escape(aid)}.*?status: active)\n(---)",
                        re.DOTALL,
                    )
                    def add_rel(m, bid=bid):
                        body = m.group(1)
                        if "related:" in body:
                            return m.group(0)
                        return f"{body}\nrelated:\n  - {bid}\n{m.group(2)}"
                    content_map[cat] = block_pat.sub(add_rel, content_map[cat])

    headers = {
        "real": (
            "# 现实问题\n\n"
            "> **回答什么**:发生过什么、是什么 — 客观经历与事实。\n"
            "> **子分类可按需新增**；校验题加 `[校验]` 标签。\n"
        ),
        "emo": (
            "# 情感问题\n\n"
            "> **回答什么**:感受什么、情绪体验、关系中的主观感受。\n"
            "> **子分类可按需新增**；校验题加 `[校验]` 标签。\n"
        ),
        "dec": (
            "# 决策问题\n\n"
            "> **回答什么**:怎么选择、怎么判断、面临取舍时的倾向。\n"
            "> **子分类可按需新增**；校验题加 `[校验]` 标签。\n"
        ),
        "sta": (
            "# 状态问题\n\n"
            "> **回答什么**:现在怎么样 — 近期压力、睡眠、动力、困扰、身心状态。\n"
            "> **子分类可按需新增**；校验题加 `[校验]` 标签。\n"
        ),
        "self": None,  # preserve existing
        "val": (
            "# 价值问题\n\n"
            "> **回答什么**:认为什么重要、底线是什么、优先级与原则。\n"
            "> **子分类可按需新增**；校验题加 `[校验]` 标签。\n"
        ),
        "oth": (
            "# 其他\n\n"
            "> **何时使用**:暂无法归入现实/情感/决策/状态/自我认知/价值六类，或需人工再判。\n"
            "> 积累到一定数量后，由人类决定是否新增一级类。\n"
        ),
    }

    # 自我认知: append after existing Q-SELF-001
    self_path = CATEGORIES / "自我认知.md"
    existing_self = self_path.read_text(encoding="utf-8")
    self_path.write_text(
        existing_self.rstrip() + "\n\n" + content_map["self"],
        encoding="utf-8",
    )

    for cat in ("real", "emo", "dec", "sta", "val", "oth"):
        path = CATEGORIES / FILE_NAMES[cat]
        path.write_text(headers[cat] + "\n" + content_map[cat], encoding="utf-8")

    print("Counts per category:")
    for cat in PREFIX:
        print(f"  {FILE_NAMES[cat]}: {counters[cat]}")
    print(f"Skipped: {len(skipped)}")
    for s in skipped:
        print(f"  {s}")


if __name__ == "__main__":
    main()
