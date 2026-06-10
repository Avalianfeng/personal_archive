export const DIMENSION_KEYS = [
  // 认知风格
  'rationality',
  'abstraction',
  'planning',
  'curiosity',
  // 情绪风格
  'anxiety',
  'empathy',
  'emotionStability',
  // 社会行为
  'extraversion',
  'independence',
  'cooperation',
  // 动机结构
  'achievementDrive',
  'securityDrive',
  'freedomDrive',
  // 价值观
  'ruleOrientation',
  'fairness',
  'loyalty',
] as const;

export type DimensionKey = (typeof DIMENSION_KEYS)[number];

export const DIMENSION_LABELS: Record<DimensionKey, string> = {
  rationality: '理性程度',
  abstraction: '抽象程度',
  planning: '规划倾向',
  curiosity: '好奇心',
  anxiety: '焦虑倾向',
  empathy: '共情能力',
  emotionStability: '情绪稳定性',
  extraversion: '外向程度',
  independence: '独立程度',
  cooperation: '合作倾向',
  achievementDrive: '成就驱动',
  securityDrive: '安全驱动',
  freedomDrive: '自由驱动',
  ruleOrientation: '规则倾向',
  fairness: '公平倾向',
  loyalty: '忠诚倾向',
};

export const DIMENSION_CATEGORIES: Record<string, DimensionKey[]> = {
  '认知风格': ['rationality', 'abstraction', 'planning', 'curiosity'],
  '情绪风格': ['anxiety', 'empathy', 'emotionStability'],
  '社会行为': ['extraversion', 'independence', 'cooperation'],
  '动机结构': ['achievementDrive', 'securityDrive', 'freedomDrive'],
  '价值观': ['ruleOrientation', 'fairness', 'loyalty'],
};
