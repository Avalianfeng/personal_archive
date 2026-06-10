import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import {
  ARCHIVE_QUESTIONS,
  buildArchive,
  renderMarkdown,
  type ArchiveAnswer,
  type ArchiveReport,
  type PersonArchive,
} from '@personal-archive/engine';

const STORAGE_KEY = 'personal_archive_draft';

interface ArchiveState {
  archiveId: string | null;
  createdAt: string | null;
  answers: ArchiveAnswer[];
  archive: PersonArchive | null;
  report: ArchiveReport | null;

  startNew: () => void;
  resumeOrStart: () => void;
  setAnswer: (answer: ArchiveAnswer) => void;
  finish: () => void;
  reset: () => void;
}

function upsertAnswer(answers: ArchiveAnswer[], answer: ArchiveAnswer): ArchiveAnswer[] {
  const idx = answers.findIndex((a) => a.questionId === answer.questionId);
  if (idx >= 0) {
    const next = [...answers];
    next[idx] = answer;
    return next;
  }
  return [...answers, answer];
}

export const useArchiveStore = create<ArchiveState>()(
  persist(
    (set, get) => ({
      archiveId: null,
      createdAt: null,
      answers: [],
      archive: null,
      report: null,

      startNew: () => {
        const now = new Date().toISOString();
        set({
          archiveId: crypto.randomUUID(),
          createdAt: now,
          answers: [],
          archive: null,
          report: null,
        });
      },

      resumeOrStart: () => {
        const { archiveId, createdAt } = get();
        if (!archiveId || !createdAt) {
          get().startNew();
        }
      },

      setAnswer: (answer) => {
        set((state) => ({
          answers: upsertAnswer(state.answers, answer),
        }));
      },

      finish: () => {
        const { answers, archiveId, createdAt } = get();
        const archive = buildArchive(answers, {
          id: archiveId ?? undefined,
          createdAt: createdAt ?? undefined,
        });
        const report = renderMarkdown(archive);
        set({ archive, report });
      },

      reset: () => {
        set({
          archiveId: null,
          createdAt: null,
          answers: [],
          archive: null,
          report: null,
        });
      },
    }),
    {
      name: STORAGE_KEY,
      partialize: (state) => ({
        archiveId: state.archiveId,
        createdAt: state.createdAt,
        answers: state.answers,
        archive: state.archive,
        report: state.report,
      }),
    },
  ),
);

export { ARCHIVE_QUESTIONS, STORAGE_KEY };
