import type {
  ArchiveAnswer,
  ArchiveData,
  ArchiveQuestion,
  PersonArchive,
} from './types';
import { ARCHIVE_QUESTIONS } from './questions';

function createEmptyData(): ArchiveData {
  return {
    basic: {},
    social: {},
    career: {},
    inner: {},
  };
}

function setNestedValue(obj: Record<string, unknown>, path: string, value: string): void {
  const parts = path.split('.');
  let current: Record<string, unknown> = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    const key = parts[i];
    if (!(key in current) || typeof current[key] !== 'object' || current[key] === null) {
      current[key] = {};
    }
    current = current[key] as Record<string, unknown>;
  }
  current[parts[parts.length - 1]] = value;
}

export function mapAnswersToData(
  answers: ArchiveAnswer[],
  questions: ArchiveQuestion[] = ARCHIVE_QUESTIONS,
): ArchiveData {
  const data = createEmptyData();
  const questionMap = new Map(questions.map((q) => [q.id, q]));

  for (const answer of answers) {
    if (answer.skipped) continue;

    const question = questionMap.get(answer.questionId);
    if (!question) continue;

    let value: string | undefined;
    if (question.type === 'choice') {
      value = answer.optionLabel;
    } else {
      value = answer.textAnswer?.trim();
    }

    if (value) {
      setNestedValue(data as unknown as Record<string, unknown>, question.mapsTo, value);
    }
  }

  return data;
}

export function computeCompleteness(
  answers: ArchiveAnswer[],
  totalQuestions: number = ARCHIVE_QUESTIONS.length,
): number {
  if (totalQuestions === 0) return 0;
  const answered = answers.filter((a) => !a.skipped).length;
  return Math.round((answered / totalQuestions) * 100) / 100;
}

export function buildArchive(
  answers: ArchiveAnswer[],
  existing?: Partial<Pick<PersonArchive, 'id' | 'createdAt'>>,
): PersonArchive {
  const now = new Date().toISOString();
  const data = mapAnswersToData(answers);

  return {
    id: existing?.id ?? crypto.randomUUID(),
    answers,
    data,
    completeness: computeCompleteness(answers),
    createdAt: existing?.createdAt ?? now,
    updatedAt: now,
  };
}
