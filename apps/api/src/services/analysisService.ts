import type { PersonalityVector, AnalysisReport } from '@renge-shenqian/shared';
import { DIMENSION_LABELS } from '@renge-shenqian/shared';
import { env } from '../config/env.js';
import db from '../db/index.js';
import type { Answer } from '@renge-shenqian/shared';

const ANALYSIS_PROMPT_VERSION = 'v1';

export async function generateAnalysis(
  vector: PersonalityVector,
  topAnswers: Answer[],
): Promise<AnalysisReport> {
  if (env.LLM_MOCK === 'true') {
    return getMockReport(vector);
  }

  return callLLM(vector, topAnswers);
}

async function callLLM(
  vector: PersonalityVector,
  topAnswers: Answer[],
): Promise<AnalysisReport> {
  const systemPrompt = `你是一个人格深潜（Personality Dive）的 AI 分析助手。
你的任务是观察和理解用户的人格特征，而非评判或诊断。
严格禁止：
- 使用 MBTI、九型人格、星座等固定标签
- 使用"高分/低分"、"正确/错误"、"好/坏"等评价性语言
- 使用心理诊断或医学建议措辞
语气：第二人称"你"、观察式叙事。`;

  const vectorDisplay = Object.entries(vector)
    .map(([key, val]) => `${DIMENSION_LABELS[key as keyof typeof DIMENSION_LABELS]}(${key}): ${val.toFixed(2)}`)
    .join('\n');

  const answersDisplay = topAnswers
    .map((a) => `题${a.questionId}: ${a.optionKey || a.textAnswer || '(未作答)'}`)
    .join('\n');

  const userPrompt = `根据以下人格向量和用户的关键回答，生成一份人格分析报告。

## 人格向量（0-1，0.5为中性）
${vectorDisplay}

## 用户关键回答
${answersDisplay}

请输出严格符合以下 JSON schema 的报告（不要输出任何其他文字）：
{
  "cognitiveStyle": "string (100-200字，描述用户如何思考、做决策、处理信息)",
  "emotionalPattern": "string (100-200字，描述用户如何处理压力和情绪)",
  "socialPattern": "string (100-200字，描述用户如何与人互动的模式)",
  "strengths": ["string 优势1", "string 优势2", "string 优势3"],
  "blindSpots": ["string 潜在盲区1", "string 潜在盲区2"],
  "growthSuggestions": ["string 成长建议1", "string 成长建议2"]
}`;

  const response = await fetch(`${env.LLM_BASE_URL}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${env.LLM_API_KEY}`,
    },
    body: JSON.stringify({
      model: env.LLM_MODEL,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt },
      ],
      temperature: 0.7,
      response_format: { type: 'json_object' },
    }),
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`LLM API error ${response.status}: ${errText}`);
  }

  const data = (await response.json()) as {
    choices: Array<{ message: { content: string } }>;
  };

  const content = data.choices[0]?.message?.content;
  if (!content) throw new Error('Empty LLM response');

  return JSON.parse(content) as AnalysisReport;
}

export function saveAnalysis(sessionId: string, report: AnalysisReport): void {
  db.prepare(
    'INSERT OR REPLACE INTO analyses (session_id, report_json, model, prompt_version) VALUES (?, ?, ?, ?)',
  ).run(sessionId, JSON.stringify(report), env.LLM_MODEL, ANALYSIS_PROMPT_VERSION);
}

export function getAnalysisForSession(sessionId: string): AnalysisReport | null {
  const row = db
    .prepare('SELECT report_json FROM analyses WHERE session_id = ?')
    .get(sessionId) as { report_json: string } | undefined;

  if (!row) return null;
  return JSON.parse(row.report_json) as AnalysisReport;
}

function getMockReport(vector: PersonalityVector): AnalysisReport {
  const highDims = Object.entries(vector)
    .filter(([, v]) => v > 0.6)
    .map(([k]) => DIMENSION_LABELS[k as keyof typeof DIMENSION_LABELS]);
  const lowDims = Object.entries(vector)
    .filter(([, v]) => v < 0.4)
    .map(([k]) => DIMENSION_LABELS[k as keyof typeof DIMENSION_LABELS]);

  return {
    cognitiveStyle:
      '你的思维兼具理性分析的条理与抽象联想的广度。面对复杂问题时，你倾向于先梳理逻辑框架，再注入直觉判断。信息处理时，你既能关注细节，也能跳出局部看到更大的图景。',
    emotionalPattern:
      '你在情绪上表现出较强的韧性与自我觉察。面对压力时，你通常能保持冷静，给情绪留出缓冲空间。你善于理解他人的感受，但也懂得在共情与自我边界之间维持平衡。',
    socialPattern:
      '在社交中，你更看重互动的质量而非数量。你倾向于选择性地投入精力，在深度交流中感到满足。独处对你而言不是孤独，而是补充能量的重要方式。',
    strengths: [
      highDims[0] ? `${highDims[0]}是你较为突出的特质，这在决策和人际中常常成为你的优势` : '自我觉察能力',
      highDims[1] ? `${highDims[1]}让你在特定情境中展现出独特的应对方式` : '适应力强',
      lowDims[0] ? `${lowDims[0]}的平衡表现让你避免了极端化倾向` : '灵活的判断力',
    ],
    blindSpots: [
      lowDims[0]
        ? `有时在${lowDims[0]}方面可能会忽略一些信号，建议在相关情境中更加留意`
        : '偶尔可能过于依赖某一种思维模式',
      highDims[0]
        ? `你较为突出的${highDims[0]}特质，在某些情境下可能让其他人产生距离感`
        : '可以尝试更主动地表达自己的想法',
    ],
    growthSuggestions: [
      '尝试在舒适区的边缘做一些微小的突破，不求改变，只在体验中丰富对自己的认知',
      '定期记录自己的决策和感受，你会发现一些有趣的行为模式',
    ],
  };
}
