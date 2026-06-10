import type { Question, PersonalityVector, AnalysisReport } from '@personal-archive/personality';

const MOCK_QUESTIONS: Question[] = [
  {
    id: 'm01',
    question: '朋友临时取消约定，你通常更接近于…',
    type: 'choice',
    options: [
      { key: 'A', label: '有些生气', weights: {} },
      { key: 'B', label: '理解对方', weights: {} },
      { key: 'C', label: '无所谓', weights: {} },
      { key: 'D', label: '问问原因', weights: {} },
    ],
    dimensions: ['emotionStability', 'empathy'],
  },
  {
    id: 'm02',
    question: '旅行时你更倾向于…',
    type: 'choice',
    options: [
      { key: 'A', label: '提前做好详细攻略', weights: {} },
      { key: 'B', label: '大概规划', weights: {} },
      { key: 'C', label: '走到哪算哪', weights: {} },
      { key: 'D', label: '看同伴的安排', weights: {} },
    ],
    dimensions: ['planning'],
  },
  {
    id: 'm03',
    question: '面对一个从未遇到过的问题，你的第一反应通常是…',
    type: 'choice',
    options: [
      { key: 'A', label: '收集资料，分析后再动手', weights: {} },
      { key: 'B', label: '先试试看，边做边调整', weights: {} },
      { key: 'C', label: '问问有经验的人', weights: {} },
      { key: 'D', label: '有点焦虑但会上', weights: {} },
    ],
    dimensions: ['rationality'],
  },
  {
    id: 'm04',
    question: '你更享受哪种社交场合？',
    type: 'choice',
    options: [
      { key: 'A', label: '热闹的聚会', weights: {} },
      { key: 'B', label: '三五好友深度聊', weights: {} },
      { key: 'C', label: '一个人安静', weights: {} },
      { key: 'D', label: '有主题的活动', weights: {} },
    ],
    dimensions: ['extraversion'],
  },
  {
    id: 'm05',
    question: '一个复杂的理论，你通常如何理解？',
    type: 'choice',
    options: [
      { key: 'A', label: '用具体例子类比', weights: {} },
      { key: 'B', label: '把握抽象框架', weights: {} },
      { key: 'C', label: '一步步拆解逻辑', weights: {} },
      { key: 'D', label: '和别人讨论', weights: {} },
    ],
    dimensions: ['abstraction'],
  },
  {
    id: 'm06',
    question: '请用一句话描述最近让你感到平静的瞬间。',
    type: 'text',
    placeholder: '描述一个场景或感受...',
    maxLength: 120,
    dimensions: ['emotionStability'],
  },
];

export function mockSessionData(): { sessionId: string; questions: Question[] } {
  return {
    sessionId: `mock-${Date.now()}`,
    questions: MOCK_QUESTIONS,
  };
}

export function mockVector(): PersonalityVector {
  return {
    rationality: 0.72,
    abstraction: 0.65,
    planning: 0.45,
    curiosity: 0.78,
    anxiety: 0.35,
    empathy: 0.68,
    emotionStability: 0.62,
    extraversion: 0.30,
    independence: 0.75,
    cooperation: 0.55,
    achievementDrive: 0.60,
    securityDrive: 0.42,
    freedomDrive: 0.70,
    ruleOrientation: 0.38,
    fairness: 0.72,
    loyalty: 0.80,
  };
}

export function mockReport(): AnalysisReport {
  return {
    cognitiveStyle:
      '你的思维兼具理性分析的条理与抽象联想的广度。面对复杂问题时，你倾向于先梳理逻辑框架，再注入直觉判断。信息处理时，你既能关注细节，也能跳出局部看到更大的图景。',
    emotionalPattern:
      '你在情绪上表现出较强的韧性与自我觉察。面对压力时，你通常能保持冷静，给情绪留出缓冲空间。你善于理解他人的感受，但也懂得在共情与自我边界之间维持平衡。',
    socialPattern:
      '在社交中，你更看重互动的质量而非数量。你倾向于选择性地投入精力，在深度交流中感到满足。独处对你而言不是孤独，而是补充能量的重要方式。',
    strengths: [
      '理性分析能力是你的突出优势，在决策和人际中常常成为可靠支撑',
      '好奇心与开放心态让你在变化中保持灵活，善于发现新的可能',
      '情感上的忠诚与共情，让你在亲密关系中建立深厚的信任',
    ],
    blindSpots: [
      '有时在社交场合可能会低估自己的影响力，建议在合适的时机更主动地表达',
      '规划倾向适中，在需要长期坚持的项目中可能需要额外的外部结构来辅助',
    ],
    growthSuggestions: [
      '尝试在舒适区的边缘做一些微小的突破，不求改变，只在体验中丰富对自己的认知',
      '定期记录自己的决策和感受，你会慢慢发现一些有趣的个人行为模式',
    ],
  };
}
