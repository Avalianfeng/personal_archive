import { create } from 'zustand';
import type { Question, Answer, PersonalityVector, AnalysisReport } from '@renge-shenqian/shared';

interface SessionStore {
  sessionId: string | null;
  questions: Question[];
  answers: Answer[];
  currentIndex: number;
  vector: PersonalityVector | null;
  report: AnalysisReport | null;
  status: 'idle' | 'active' | 'completed';

  setSession: (sessionId: string, questions: Question[]) => void;
  addAnswer: (answer: Answer) => void;
  nextQuestion: () => void;
  prevQuestion: () => void;
  setResult: (vector: PersonalityVector, report: AnalysisReport | null) => void;
  reset: () => void;
}

export const useSessionStore = create<SessionStore>((set, get) => ({
  sessionId: null,
  questions: [],
  answers: [],
  currentIndex: 0,
  vector: null,
  report: null,
  status: 'idle',

  setSession: (sessionId, questions) =>
    set({ sessionId, questions, answers: [], currentIndex: 0, status: 'active', vector: null, report: null }),

  addAnswer: (answer) => {
    const { answers } = get();
    const existing = answers.findIndex((a) => a.questionId === answer.questionId);
    const next = [...answers];
    if (existing >= 0) {
      next[existing] = answer;
    } else {
      next.push(answer);
    }
    set({ answers: next });
  },

  nextQuestion: () => {
    const { currentIndex, questions } = get();
    if (currentIndex < questions.length - 1) {
      set({ currentIndex: currentIndex + 1 });
    }
  },

  prevQuestion: () => {
    const { currentIndex } = get();
    if (currentIndex > 0) {
      set({ currentIndex: currentIndex - 1 });
    }
  },

  setResult: (vector, report) =>
    set({ vector, report, status: 'completed' }),

  reset: () =>
    set({
      sessionId: null,
      questions: [],
      answers: [],
      currentIndex: 0,
      vector: null,
      report: null,
      status: 'idle',
    }),
}));
