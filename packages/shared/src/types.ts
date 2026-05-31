import type { DimensionKey } from './dimensions';

export interface Question {
  id: string;
  question: string;
  type: 'choice' | 'text';
  options?: ChoiceOption[];
  dimensions: DimensionKey[];
  /** placeholder for text-type questions */
  placeholder?: string;
  maxLength?: number;
}

export interface ChoiceOption {
  key: string;
  label: string;
  weights: Partial<Record<DimensionKey, number>>;
}

export type PersonalityVector = Record<DimensionKey, number>;

export interface Answer {
  questionId: string;
  optionKey?: string;
  textAnswer?: string;
}

export interface AnalysisReport {
  cognitiveStyle: string;
  emotionalPattern: string;
  socialPattern: string;
  strengths: string[];
  blindSpots: string[];
  growthSuggestions: string[];
}

export interface SessionState {
  id: string;
  questions: Question[];
  answers: Answer[];
  vector: PersonalityVector | null;
  report: AnalysisReport | null;
  status: 'active' | 'completed';
  createdAt: string;
  completedAt: string | null;
}
