import { DIMENSION_KEYS } from './dimensions';
import type { PersonalityVector, Answer, ChoiceOption } from './types';

export function createInitialVector(): PersonalityVector {
  const entries = DIMENSION_KEYS.map((key) => [key, 0.5] as const);
  return Object.fromEntries(entries) as PersonalityVector;
}

export function applyAnswer(
  vector: PersonalityVector,
  option: ChoiceOption,
): PersonalityVector {
  const next = { ...vector };
  for (const [dim, weight] of Object.entries(option.weights)) {
    if (dim in next) {
      next[dim as keyof PersonalityVector] = clamp(
        next[dim as keyof PersonalityVector] + weight,
        0,
        1,
      );
    }
  }
  return next;
}

export function finalizeVector(
  answers: Answer[],
  optionsMap: Map<string, ChoiceOption[]>,
): PersonalityVector {
  const vector = createInitialVector();
  for (const answer of answers) {
    if (!answer.optionKey) continue;
    const options = optionsMap.get(answer.questionId);
    if (!options) continue;
    const selected = options.find((o) => o.key === answer.optionKey);
    if (!selected) continue;
    for (const [dim, weight] of Object.entries(selected.weights)) {
      if (dim in vector) {
        vector[dim as keyof PersonalityVector] = clamp(
          vector[dim as keyof PersonalityVector] + weight,
          0,
          1,
        );
      }
    }
  }
  return vector;
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}
