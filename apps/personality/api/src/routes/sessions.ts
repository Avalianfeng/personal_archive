import { FastifyInstance } from 'fastify';
import { randomUUID } from 'crypto';
import db from '../db/index.js';
import { getQuestionsForSession } from '../services/questionService.js';
import { saveAnswer, computeVectorForSession } from '../services/answerService.js';
import {
  generateAnalysis,
  saveAnalysis,
  getAnalysisForSession,
} from '../services/analysisService.js';
import type { PersonalityVector } from '@personal-archive/personality';

export async function sessionRoutes(app: FastifyInstance) {
  // 创建会话
  app.post('/sessions', async (_req, reply) => {
    const sessionId = randomUUID();
    const questions = getQuestionsForSession(20);

    db.prepare('INSERT INTO sessions (id) VALUES (?)').run(sessionId);

    // 只返回 id 列表和题目正文（不含 weights）
    return reply.send({
      sessionId,
      questions: questions.map((q) => ({
        id: q.id,
        question: q.question,
        type: q.type,
        options: q.options?.map((o) => ({ key: o.key, label: o.label })),
        dimensions: q.dimensions,
        placeholder: q.placeholder,
        maxLength: q.maxLength,
      })),
    });
  });

  // 获取会话详情
  app.get<{ Params: { id: string } }>('/sessions/:id', async (req, reply) => {
    const session = db
      .prepare('SELECT * FROM sessions WHERE id = ?')
      .get(req.params.id) as Record<string, unknown> | undefined;

    if (!session) {
      return reply.status(404).send({ error: 'Session not found' });
    }

    const answers = db
      .prepare('SELECT question_id, option_key, text_answer FROM answers WHERE session_id = ?')
      .all(req.params.id) as Array<{
      question_id: string;
      option_key: string | null;
      text_answer: string | null;
    }>;

    return reply.send({
      id: session.id,
      status: session.status,
      vector: session.vector_json ? JSON.parse(session.vector_json as string) : null,
      answers: answers.map((a) => ({
        questionId: a.question_id,
        optionKey: a.option_key ?? undefined,
        textAnswer: a.text_answer ?? undefined,
      })),
      createdAt: session.created_at,
      completedAt: session.completed_at,
    });
  });

  // 提交答案
  app.post<{
    Params: { id: string };
    Body: { questionId: string; optionKey?: string; textAnswer?: string };
  }>('/sessions/:id/answers', async (req, reply) => {
    const session = db
      .prepare('SELECT * FROM sessions WHERE id = ?')
      .get(req.params.id) as Record<string, unknown> | undefined;

    if (!session) {
      return reply.status(404).send({ error: 'Session not found' });
    }

    if (session.status !== 'active') {
      return reply.status(400).send({ error: 'Session already completed' });
    }

    const { questionId, optionKey, textAnswer } = req.body;
    saveAnswer(req.params.id, questionId, optionKey, textAnswer);

    // 实时更新向量草稿
    const allAnswers = db
      .prepare('SELECT question_id, option_key, text_answer FROM answers WHERE session_id = ?')
      .all(req.params.id) as Array<{
      question_id: string;
      option_key: string | null;
      text_answer: string | null;
    }>;

    return reply.send({
      answeredCount: allAnswers.length,
    });
  });

  // 完成会话
  app.post<{ Params: { id: string } }>('/sessions/:id/complete', async (req, reply) => {
    const session = db
      .prepare('SELECT * FROM sessions WHERE id = ?')
      .get(req.params.id) as Record<string, unknown> | undefined;

    if (!session) {
      return reply.status(404).send({ error: 'Session not found' });
    }

    // 计算向量
    const vector = computeVectorForSession(req.params.id);

    // 尝试 LLM 分析
    let report;
    try {
      const allAnswers = db
        .prepare('SELECT question_id, option_key, text_answer FROM answers WHERE session_id = ? ORDER BY answered_at DESC LIMIT 10')
        .all(req.params.id) as Array<{
        question_id: string;
        option_key: string | null;
        text_answer: string | null;
      }>;

      const topAnswers = allAnswers.map((a) => ({
        questionId: a.question_id,
        optionKey: a.option_key ?? undefined,
        textAnswer: a.text_answer ?? undefined,
      }));

      report = await generateAnalysis(vector, topAnswers);
      saveAnalysis(req.params.id, report);
    } catch (err) {
      report = null;
    }

    // 标记完成
    db.prepare(
      'UPDATE sessions SET status = ?, vector_json = ?, completed_at = datetime(\'now\') WHERE id = ?',
    ).run('completed', JSON.stringify(vector), req.params.id);

    return reply.send({
      vector,
      report,
      reportPending: report === null,
    });
  });

  // 获取结果
  app.get<{ Params: { id: string } }>('/sessions/:id/result', async (req, reply) => {
    const session = db
      .prepare('SELECT * FROM sessions WHERE id = ?')
      .get(req.params.id) as Record<string, unknown> | undefined;

    if (!session) {
      return reply.status(404).send({ error: 'Session not found' });
    }

    const vector: PersonalityVector | null = session.vector_json
      ? (JSON.parse(session.vector_json as string) as PersonalityVector)
      : null;

    const report = getAnalysisForSession(req.params.id);

    return reply.send({
      vector,
      report,
      completedAt: session.completed_at,
    });
  });
}
