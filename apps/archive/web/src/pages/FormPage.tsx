import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ARCHIVE_QUESTIONS, useArchiveStore } from '../store/useArchiveStore';
import type { ArchiveAnswer } from '@personal-archive/engine';

function getDraft(
  answers: ArchiveAnswer[],
  questionId: string,
): { optionKey?: string; textAnswer?: string } {
  const a = answers.find((item) => item.questionId === questionId);
  if (!a || a.skipped) return {};
  return { optionKey: a.optionKey, textAnswer: a.textAnswer };
}

export default function FormPage() {
  const navigate = useNavigate();
  const { answers, archive, resumeOrStart, setAnswer, finish } = useArchiveStore();
  const [drafts, setDrafts] = useState<Record<string, { optionKey?: string; textAnswer?: string }>>({});

  useEffect(() => {
    resumeOrStart();
  }, [resumeOrStart]);

  useEffect(() => {
    if (archive) navigate('/report');
  }, [archive, navigate]);

  useEffect(() => {
    const initial: Record<string, { optionKey?: string; textAnswer?: string }> = {};
    for (const q of ARCHIVE_QUESTIONS) {
      initial[q.id] = getDraft(answers, q.id);
    }
    setDrafts(initial);
  }, [answers]);

  const answeredCount = useMemo(() => {
    return Object.values(drafts).filter(
      (d) => d.optionKey || d.textAnswer?.trim(),
    ).length;
  }, [drafts]);

  const updateDraft = (questionId: string, patch: Partial<{ optionKey?: string; textAnswer?: string }>) => {
    setDrafts((prev) => ({
      ...prev,
      [questionId]: { ...prev[questionId], ...patch },
    }));
  };

  const skipQuestion = (questionId: string) => {
    setAnswer({ questionId, skipped: true });
    setDrafts((prev) => ({ ...prev, [questionId]: {} }));
  };

  const handleSubmit = () => {
    for (const q of ARCHIVE_QUESTIONS) {
      const draft = drafts[q.id] ?? {};
      const hasOption = Boolean(draft.optionKey);
      const hasText = Boolean(draft.textAnswer?.trim());

      if (!hasOption && !hasText) {
        setAnswer({ questionId: q.id, skipped: true });
        continue;
      }

      if (q.type === 'choice' && draft.optionKey) {
        const option = q.options?.find((o) => o.key === draft.optionKey);
        setAnswer({
          questionId: q.id,
          skipped: false,
          optionKey: draft.optionKey,
          optionLabel: option?.label,
          textAnswer: draft.textAnswer?.trim() || undefined,
        });
      } else if (q.type === 'text' && hasText) {
        setAnswer({
          questionId: q.id,
          skipped: false,
          textAnswer: draft.textAnswer!.trim(),
        });
      } else if (hasText) {
        setAnswer({
          questionId: q.id,
          skipped: false,
          textAnswer: draft.textAnswer!.trim(),
        });
      } else {
        setAnswer({ questionId: q.id, skipped: true });
      }
    }
    finish();
  };

  return (
    <div className="min-h-screen bg-paper">
      <header className="sticky top-0 z-10 bg-paper/95 backdrop-blur border-b border-border px-6 py-4">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-ink">个人档案</h1>
            <p className="text-xs text-ink-muted mt-0.5">
              已填写 {answeredCount} / {ARCHIVE_QUESTIONS.length} 题 · 未填项可跳过
            </p>
          </div>
          <button
            onClick={handleSubmit}
            className="px-5 py-2 rounded-lg bg-accent text-white text-sm font-medium
                       hover:bg-accent-hover transition-colors"
          >
            生成报告
          </button>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-6 py-10 space-y-10">
        {ARCHIVE_QUESTIONS.map((q, index) => {
          const draft = drafts[q.id] ?? {};
          return (
            <section key={q.id} className="border border-border rounded-2xl p-6 bg-white">
              <div className="flex items-start justify-between gap-4 mb-4">
                <h2 className="text-base font-medium text-ink leading-snug">
                  <span className="text-ink-faint mr-2">{index + 1}.</span>
                  {q.question}
                </h2>
                <button
                  type="button"
                  onClick={() => skipQuestion(q.id)}
                  className="text-xs text-ink-faint hover:text-ink shrink-0"
                >
                  跳过
                </button>
              </div>

              {q.type === 'choice' && q.options && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {q.options.map((opt) => (
                    <button
                      key={opt.key}
                      type="button"
                      onClick={() => updateDraft(q.id, { optionKey: opt.key })}
                      className={`px-4 py-2 rounded-lg border text-sm transition-all
                        ${
                          draft.optionKey === opt.key
                            ? 'border-accent bg-accent/5 text-ink ring-1 ring-accent/30'
                            : 'border-border text-ink-muted hover:border-ink-faint'
                        }`}
                    >
                      {opt.label}
                    </button>
                  ))}
                </div>
              )}

              <textarea
                value={draft.textAnswer ?? ''}
                onChange={(e) => {
                  const maxLen = q.maxLength ?? 300;
                  if (e.target.value.length <= maxLen) {
                    updateDraft(q.id, { textAnswer: e.target.value });
                  }
                }}
                placeholder={
                  q.type === 'choice'
                    ? '补充说明（可选）'
                    : q.placeholder ?? '在此输入…'
                }
                className="w-full min-h-[88px] p-3 rounded-xl border border-border
                           text-ink placeholder:text-ink-faint text-sm leading-relaxed
                           focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/20
                           resize-y transition-colors"
              />
              <div className="text-right text-xs text-ink-faint mt-1">
                {(draft.textAnswer ?? '').length}/{q.maxLength ?? 300}
              </div>
            </section>
          );
        })}

        <div className="flex justify-end pb-12">
          <button
            onClick={handleSubmit}
            className="px-8 py-3 rounded-lg bg-accent text-white font-medium
                       hover:bg-accent-hover transition-colors"
          >
            生成报告
          </button>
        </div>
      </main>
    </div>
  );
}
