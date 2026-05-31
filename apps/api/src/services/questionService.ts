import { readFileSync, existsSync, readdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import type { Question } from '@renge-shenqian/shared';
import { selectQuestions } from '@renge-shenqian/shared';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = resolve(__dirname, '../../data/questions');

let questionBank: Question[] | null = null;

export function loadQuestionBankSync(): Question[] {
  if (questionBank) return questionBank;

  const all: Question[] = [];

  // 优先按文件名加载
  const priorityFiles = ['sample-20.json'];
  for (const file of priorityFiles) {
    const path = resolve(dataDir, file);
    if (existsSync(path)) {
      const raw = readFileSync(path, 'utf-8');
      all.push(...JSON.parse(raw));
    }
  }

  // 如果优先文件不够，扫描目录
  if (all.length === 0 && existsSync(dataDir)) {
    const entries = readdirSync(dataDir);
    for (const entry of entries) {
      if (entry.endsWith('.json')) {
        const raw = readFileSync(resolve(dataDir, entry), 'utf-8');
        all.push(...JSON.parse(raw));
      }
    }
  }

  questionBank = all;
  return all;
}

export async function loadQuestionBank(): Promise<Question[]> {
  return loadQuestionBankSync();
}

export function getQuestionsForSession(count: number): Question[] {
  const bank = loadQuestionBankSync();
  return selectQuestions(bank, count);
}
