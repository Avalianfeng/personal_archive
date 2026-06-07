import type { Question, PersonalityVector, AnalysisReport } from '@renge-shenqian/shared';

const BASE_URL = '/api';

interface SessionResponse {
  sessionId: string;
  questions: Question[];
}

interface CompleteResponse {
  vector: PersonalityVector;
  report: AnalysisReport | null;
  reportPending: boolean;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const method = options?.method ?? 'GET';
  const needsJsonBody = method !== 'GET' && method !== 'HEAD' && options?.body === undefined;

  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    body: needsJsonBody ? '{}' : options?.body,
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}

export const api = {
  createSession: () => request<SessionResponse>('/sessions', { method: 'POST' }),

  submitAnswer: (sessionId: string, questionId: string, optionKey?: string, textAnswer?: string) =>
    request(`/sessions/${sessionId}/answers`, {
      method: 'POST',
      body: JSON.stringify({ questionId, optionKey, textAnswer }),
    }),

  completeSession: (sessionId: string) =>
    request<CompleteResponse>(`/sessions/${sessionId}/complete`, { method: 'POST' }),

  getResult: (sessionId: string) =>
    request<{ vector: PersonalityVector; report: AnalysisReport | null }>(
      `/sessions/${sessionId}/result`,
    ),
};
