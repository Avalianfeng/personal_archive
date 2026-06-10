import db from '../db/index.js';
import type { Answer, PersonalityVector } from '@personal-archive/personality';
import { finalizeVector } from '@personal-archive/personality';
import { loadQuestionBankSync } from './questionService.js';
import type { ChoiceOption } from '@personal-archive/personality';

export function saveAnswer(
  sessionId: string,
  questionId: string,
  optionKey?: string,
  textAnswer?: string,
): void {
  const stmt = db.prepare(
    'INSERT INTO answers (session_id, question_id, option_key, text_answer) VALUES (?, ?, ?, ?)',
  );
  stmt.run(sessionId, questionId, optionKey || null, textAnswer || null);
}

export function getAnswersForSession(sessionId: string): Answer[] {
  const rows = db
    .prepare('SELECT question_id, option_key, text_answer FROM answers WHERE session_id = ?')
    .all(sessionId) as Array<{ question_id: string; option_key: string | null; text_answer: string | null }>;

  return rows.map((row) => ({
    questionId: row.question_id,
    optionKey: row.option_key ?? undefined,
    textAnswer: row.text_answer ?? undefined,
  }));
}

export function computeVectorForSession(sessionId: string): PersonalityVector {
  const answers = getAnswersForSession(sessionId);
  const bank = loadQuestionBankSync();

  const optionsMap = new Map<string, ChoiceOption[]>();
  for (const q of bank) {
    if (q.type === 'choice' && q.options) {
      optionsMap.set(q.id, q.options);
    }
  }

  const vector = finalizeVector(answers, optionsMap);

  // 持久化向量
  db.prepare('UPDATE sessions SET vector_json = ? WHERE id = ?').run(
    JSON.stringify(vector),
    sessionId,
  );

  return vector;
}
