import type { Question } from './types';
import type { DimensionKey } from './dimensions';
import { DIMENSION_KEYS } from './dimensions';

export function selectQuestions(questionBank: Question[], count: number): Question[] {
  const shuffled = [...questionBank].sort(() => Math.random() - 0.5);

  const byDimension = new Map<DimensionKey, Question[]>();
  for (const dim of DIMENSION_KEYS) {
    byDimension.set(dim, []);
  }
  for (const q of shuffled) {
    for (const dim of q.dimensions) {
      byDimension.get(dim)?.push(q);
    }
  }

  const selected: Question[] = [];
  const usedIds = new Set<string>();

  // 每个维度至少 1 题
  for (const dim of DIMENSION_KEYS) {
    const candidates = byDimension.get(dim) || [];
    for (const q of candidates) {
      if (!usedIds.has(q.id)) {
        selected.push(q);
        usedIds.add(q.id);
        break;
      }
    }
  }

  // 剩余名额从随机顺序补充（优先未覆盖维度的题）
  const remaining = shuffled.filter((q) => !usedIds.has(q.id));
  for (const q of remaining) {
    if (selected.length >= count) break;
    selected.push(q);
    usedIds.add(q.id);
  }

  // 按维度轮转打乱顺序，避免同类连问
  const sorted = sortByDimensionRoundRobin(selected);

  return sorted.slice(0, count);
}

function sortByDimensionRoundRobin(questions: Question[]): Question[] {
  const dimQueues = new Map<DimensionKey, Question[]>();
  for (const q of questions) {
    const primaryDim = q.dimensions[0];
    if (!dimQueues.has(primaryDim)) dimQueues.set(primaryDim, []);
    dimQueues.get(primaryDim)!.push(q);
  }

  const result: Question[] = [];
  const dims = [...dimQueues.keys()];
  let index = 0;

  while (result.length < questions.length) {
    const dim = dims[index % dims.length];
    const queue = dimQueues.get(dim);
    if (queue && queue.length > 0) {
      result.push(queue.shift()!);
    }
    index++;
  }

  return result;
}
