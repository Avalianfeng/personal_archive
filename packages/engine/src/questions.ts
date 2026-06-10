import type { ArchiveQuestion } from './types';
import questionsData from '../../../plugins/core-intake/questions.json';

export const ARCHIVE_QUESTIONS: ArchiveQuestion[] = questionsData as ArchiveQuestion[];

export function getQuestionById(id: string): ArchiveQuestion | undefined {
  return ARCHIVE_QUESTIONS.find((q) => q.id === id);
}
