export { DIMENSION_KEYS, DIMENSION_LABELS, DIMENSION_CATEGORIES } from './dimensions';
export type { DimensionKey } from './dimensions';

export type {
  Question,
  ChoiceOption,
  PersonalityVector,
  Answer,
  AnalysisReport,
  SessionState,
} from './types';

export { createInitialVector, applyAnswer, finalizeVector } from './scoring';
export { selectQuestions } from './selection';
